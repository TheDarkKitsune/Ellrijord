init -1 python:
    class Inventory(object):
        def __init__(self, slot_count=28, unlocked_slots=7, max_items_per_slot=99):
            self.slot_count = int(slot_count)
            self.unlocked_slots = int(unlocked_slots)
            self.max_items_per_slot = int(max_items_per_slot)
            self.slots = [{} for _ in range(self.slot_count)]

        def _normalize_item(self, item):
            return str(item).strip().lower().replace(" ", "_")

        def _display_name(self, item):
            return str(item).replace("_", " ").title()

        def _icon_path(self, item):
            normalized = self._normalize_item(item)
            normalized_path = "components/inventory_system/icons/{}.png".format(normalized)
            if renpy.loadable(normalized_path):
                return normalized_path
            icon_name = normalized.replace("_", " ").title().replace(" ", "")
            return "components/inventory_system/icons/{}.png".format(icon_name)

        def add_item(self, item, quantity=1, notify=True, label=None):
            item = self._normalize_item(item)
            quantity = int(quantity)
            item_label = label or self._display_name(item)

            if self.unlocked_slots <= 0:
                if notify:
                    pm_notify("No unlocked slots available.", sound_type="error")
                return 0

            if quantity <= 0:
                return 0

            original_quantity = quantity

            for slot in range(self.unlocked_slots):
                if item in self.slots[slot]:
                    space_left = self.max_items_per_slot - self.slots[slot][item]
                    if space_left <= 0:
                        continue
                    add_quantity = min(quantity, space_left)
                    self.slots[slot][item] += add_quantity
                    quantity -= add_quantity
                    if quantity <= 0:
                        if notify:
                            pm_notify("Added {} x{}.".format(item_label, original_quantity), sound_type="success")
                        return original_quantity

            for slot in range(self.unlocked_slots):
                if self.slots[slot]:
                    continue
                add_quantity = min(quantity, self.max_items_per_slot)
                self.slots[slot][item] = add_quantity
                quantity -= add_quantity
                if quantity <= 0:
                    if notify:
                        pm_notify("Added {} x{}.".format(item_label, original_quantity), sound_type="success")
                    return original_quantity

            added_total = original_quantity - quantity
            if added_total > 0:
                if notify:
                    pm_notify("Inventory full. Added {} x{}.".format(item_label, added_total), sound_type="error")
            else:
                if notify:
                    pm_notify("Could not add {} - no slots available.".format(item_label), sound_type="error")
            return added_total

        def remove_item(self, item, quantity=1):
            item = self._normalize_item(item)
            quantity = int(quantity)
            if quantity <= 0:
                pm_notify("Invalid quantity to remove.", sound_type="error")
                return 0

            original_quantity = quantity

            for slot in range(self.slot_count):
                if item not in self.slots[slot]:
                    continue
                if quantity >= self.slots[slot][item]:
                    quantity -= self.slots[slot][item]
                    del self.slots[slot][item]
                else:
                    self.slots[slot][item] -= quantity
                    quantity = 0
                if quantity <= 0:
                    break

            removed_total = original_quantity - quantity
            self.sort_inventory()

            if removed_total <= 0:
                pm_notify("Could not remove {}.".format(self._display_name(item)), sound_type="error")
                return 0

            if quantity > 0:
                pm_notify("Removed {} x{}, but some were missing.".format(self._display_name(item), removed_total), sound_type="error")
            else:
                pm_notify("Removed {} x{}.".format(self._display_name(item), removed_total), sound_type="remove")
            return removed_total

        def sort_inventory(self):
            filled_slots = [slot for slot in self.slots if slot]
            empty_slots = [{} for _ in range(max(0, self.slot_count - len(filled_slots)))]
            self.slots = filled_slots + empty_slots

        def increase_slot_count(self, additional_slots):
            additional_slots = int(additional_slots)
            if additional_slots <= 0:
                return
            self.slot_count += additional_slots
            self.slots.extend([{} for _ in range(additional_slots)])
            pm_notify("Slot count increased by {}.".format(additional_slots), sound_type="success")

        def unlock_slots(self, count):
            count = int(count)
            if count <= 0:
                return
            self.unlocked_slots = min(self.slot_count, self.unlocked_slots + count)
            pm_notify("Unlocked {} new slots.".format(count), sound_type="success")

        def lock_slots(self, count):
            count = int(count)
            if count <= 0:
                return
            if count > self.unlocked_slots:
                pm_notify("Not enough unlocked slots to lock.", sound_type="error")
                return
            self.unlocked_slots -= count
            pm_notify("Warning: slots are locked!", sound_type="error")

        def is_slot_unlocked(self, slot):
            return int(slot) < self.unlocked_slots

        def get_items(self):
            return self.slots

        def has_item(self, item, quantity=1):
            item = self._normalize_item(item)
            quantity = int(quantity)
            total = 0
            for slot in self.slots:
                if item in slot:
                    total += slot[item]
            return total >= quantity

        def total_item_count(self):
            total = 0
            for slot in self.slots:
                for quantity in slot.values():
                    total += quantity
            return total

        def reset(self, slot_count=None, unlocked_slots=None):
            if slot_count is not None:
                self.slot_count = int(slot_count)
            if unlocked_slots is not None:
                self.unlocked_slots = int(unlocked_slots)
            self.unlocked_slots = min(self.unlocked_slots, self.slot_count)
            self.slots = [{} for _ in range(self.slot_count)]

        def ensure_shape(self, slot_count=None, unlocked_slots=None, clear_items=False):
            target_slots = int(slot_count) if slot_count is not None else self.slot_count
            target_unlocked = int(unlocked_slots) if unlocked_slots is not None else self.unlocked_slots

            current_items = []
            if not clear_items:
                for slot in self.slots:
                    if slot:
                        current_items.append(dict(slot))

            self.slot_count = target_slots
            self.unlocked_slots = min(target_unlocked, self.slot_count)
            self.slots = [{} for _ in range(self.slot_count)]

            if not clear_items:
                for idx, slot in enumerate(current_items[:self.slot_count]):
                    self.slots[idx] = slot

default inventory = Inventory(slot_count=28, unlocked_slots=7)

label ell_inventory_reset_once:
    $ inventory.reset(28, 7)
    return
