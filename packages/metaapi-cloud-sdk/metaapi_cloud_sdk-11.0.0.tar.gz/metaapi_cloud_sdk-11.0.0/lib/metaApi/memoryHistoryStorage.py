from .models import MetatraderDeal, MetatraderOrder
from typing import List
from .memoryHistoryStorageModel import MemoryHistoryStorageModel
from .historyFileManager import HistoryFileManager
from datetime import datetime
from .models import date
import pytz


class MemoryHistoryStorage(MemoryHistoryStorageModel):
    """History storage which stores MetaTrader history in RAM."""

    def __init__(self, account_id: str, application: str = 'MetaApi'):
        """Inits the in-memory history store instance"""
        super().__init__()
        self._accountId = account_id
        self._fileManager = HistoryFileManager(account_id, application, self)
        self._deals = []
        self._historyOrders = []
        self._fileManager.start_update_job()

    @property
    def deals(self) -> List[MetatraderDeal]:
        """Returns all deals stored in history storage.

        Returns:
            All deals stored in history storage.
        """
        return self._deals

    @property
    def history_orders(self) -> List[MetatraderOrder]:
        """Returns all history orders stored in history storage.

        Returns:
            All history orders stored in history storage.
        """
        return self._historyOrders

    def reset(self):
        """Resets the storage. Intended for use in tests."""

        self._deals = []
        self._historyOrders = []
        self._fileManager.delete_storage_from_disk()

    async def load_data_from_disk(self):
        """Loads history data from the file manager.

        Returns:
            A coroutine which resolves when the history is loaded.
        """
        history = await self._fileManager.get_history_from_disk()
        self._deals = history['deals']
        self._historyOrders = history['historyOrders']

    async def update_disk_storage(self):
        """Saves unsaved history items to disk storage.

        Returns:
            A coroutine which resolves when the history is saved.
        """
        await self._fileManager.update_disk_storage()

    async def last_history_order_time(self) -> datetime:
        """Returns the time of the last history order record stored in the history storage.

        Returns:
            The time of the last history order record stored in the history storage
        """
        filtered_orders = list(filter(lambda order: 'doneTime' in order, self._historyOrders))
        return max(order['doneTime'] if isinstance(order['doneTime'], datetime) else date(order['doneTime']) for order
                   in (filtered_orders + [{'doneTime': datetime.fromtimestamp(0).replace(tzinfo=pytz.UTC)}]))

    async def last_deal_time(self) -> datetime:
        """Returns the time of the last history deal record stored in the history storage.

        Returns:
            The time of the last history deal record stored in the history storage.
        """
        filtered_deals = list(filter(lambda order: 'time' in order, self._deals))
        return max(deal['time'] if isinstance(deal['time'], datetime) else date(deal['time']) for deal in
                   (filtered_deals + [{'time': datetime.fromtimestamp(0).replace(tzinfo=pytz.UTC)}]))

    async def on_history_order_added(self, history_order: MetatraderOrder):
        """Invoked when a new MetaTrader history order is added.

        Args:
            history_order: New MetaTrader history order.
        """
        insert_index = 0
        replacement_index = -1

        def get_done_time(order):
            if 'doneTime' in order:
                return order['doneTime'].timestamp() if (isinstance(order['doneTime'], datetime)) \
                    else date(order['doneTime']).timestamp()
            else:
                return 0

        history_order_time = get_done_time(history_order)

        for i in range(len(self._historyOrders)):
            index = len(self._historyOrders) - 1 - i
            order = self._historyOrders[index]
            order_time = get_done_time(order)
            if (order_time < history_order_time) or \
               (order_time == history_order_time and order['id'] <= history_order['id']):
                if (order_time == history_order_time and order['id'] == history_order['id'] and
                   order['type'] == history_order['type']):
                    replacement_index = index
                else:
                    insert_index = index + 1
                break
        if replacement_index != -1:
            self._historyOrders[replacement_index] = history_order
            self._fileManager.set_start_new_order_index(replacement_index)
        else:
            self._historyOrders.insert(insert_index, history_order)
            self._fileManager.set_start_new_order_index(insert_index)

    async def on_deal_added(self, new_deal: MetatraderDeal):
        """Invoked when a new MetaTrader history deal is added.

        Args:
            new_deal: New MetaTrader history deal.
        """
        insert_index = 0
        replacement_index = -1

        def get_time(deal):
            if 'time' in deal:
                return deal['time'].timestamp() if (isinstance(deal['time'], datetime)) \
                    else date(deal['time']).timestamp()
            else:
                return 0

        new_deal_time = get_time(new_deal)
        for i in range(len(self._deals)):
            index = len(self._deals) - 1 - i
            deal = self._deals[index]
            deal_time = get_time(deal)
            if (deal_time < new_deal_time) or \
                    (deal_time == new_deal_time and deal['id'] <= new_deal['id']):
                if (deal_time == new_deal_time and deal['id'] == new_deal['id'] and
                        deal['type'] == new_deal['type']):
                    replacement_index = index
                else:
                    insert_index = index + 1
                break
        if replacement_index != -1:
            self._deals[replacement_index] = new_deal
            self._fileManager.set_start_new_deal_index(replacement_index)
        else:
            self._deals.insert(insert_index, new_deal)
            self._fileManager.set_start_new_deal_index(insert_index)
