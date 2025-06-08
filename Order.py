class AVLNode:
    def __init__(self, priority, order=None):
        self.priority = priority
        self.orders = [order] if order else []
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root, priority, order):
        if not root:
            return AVLNode(priority, order)
        elif priority < root.priority:
            root.left = self.insert(root.left, priority, order)
        elif priority > root.priority:
            root.right = self.insert(root.right, priority, order)
        else:
            root.orders.append(order)
            return root
        
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        
        balance = self.get_balance(root)
        if balance > 1 and priority < root.left.priority:
            return self.right_rotate(root)
        if balance < -1 and priority > root.right.priority:
            return self.left_rotate(root)
        if balance > 1 and priority > root.left.priority:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and priority < root.right.priority:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        
        return root

    def remove(self, node, priority, order=None):
        if not node:
            return node

        if priority < node.priority:
            node.left = self.remove(node.left, priority, order)
        elif priority > node.priority:
            node.right = self.remove(node.right, priority, order)
        else:
            if order:
                try:
                    node.orders.remove(order)
                    if not node.orders:
                        node = self._remove_node(node)
                except ValueError:
                    pass
            else:
                node = self._remove_node(node)

        if node is None:
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        balance = self.get_balance(node)
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def _remove_node(self, node):
        if node.left is None:
            return node.right
        elif node.right is None:
            return node.left

        temp = self.get_min_value_node(node.right)
        node.priority = temp.priority
        node.orders = temp.orders
        node.right = self.remove(node.right, temp.priority)

        return node

    def get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def in_order_traversal(self, node=None, result=None):
        if node is None:
            node = self.root
        if result is None:
            result = []
        if node:
            self.in_order_traversal(node.left, result)
            for order in node.orders:
                result.append(order)
            self.in_order_traversal(node.right, result)
        return result


class Order:
    def __init__(self, order_id, system_time, value, delivery_time):
        self.order_id = order_id
        self.system_time = system_time
        self.value = value
        self.delivery_time = delivery_time
        self.priority = 0.3 * (value / 50) - 0.7 * system_time
        self.ETA = system_time + delivery_time


class OrderManagementSystem:
    def __init__(self):
        self.orders = {}
        self.priority_tree = AVLTree()

    def print_order(self, order_id):
        if order_id in self.orders:
            order = self.orders[order_id]
            print(f"Order {order.order_id} has been delivered at time {order.system_time}")

    def print_orders_in_time_range(self, time1, time2):
        sorted_orders = []

    def get_rank_of_order(self, order_id):
        pass

    def create_order(self, order_id, system_time, value, delivery_time):
        new_order = Order(order_id, system_time, value, delivery_time)
        self.orders[order_id] = new_order
        self.priority_tree.root = self.priority_tree.insert(self.priority_tree.root, new_order.priority, new_order)

    def cancel_order(self, order_id):
        pass

    def update_time(self, order_id, new_delivery_time):
        pass

    def recalculate_ETAs(self):
        pass


def process_command(oms, command_line):
    parts = command_line.strip().split(',')
    command = parts[0]

    if command == "print_order":
        oms.print_order(int(parts[1]))
    elif command == "print_orders_in_time_range":
        oms.print_orders_in_time_range(int(parts[1]), int(parts[2]))
    elif command == "get_rank_of_order":
        oms.get_rank_of_order(int(parts[1]))
    elif command == "create_order":
        oms.create_order(int(parts[1]), int(parts[2]), float(parts[3]), int(parts[4]))
    elif command == "cancel_order":
        oms.cancel_order(int(parts[1]))
    elif command == "update_time":
        oms.update_time(int(parts[1]), int(parts[2]))
    else:
        print(f"Unknown command: {command}")


def main():
    oms = OrderManagementSystem()

    with open(r"C:\Users\Asna maheen\OneDrive\Desktop\Maheen_Asna\input_file.txt", 'r') as input_file:
        input_commands = input_file.readlines()

    output_lines = []

    for command in input_commands:
        parts = command.strip().split('(')
        action = parts[0]
        parameters = parts[1][:-1].split(',')

        if action == "createOrder":
            order_id, system_time, value, delivery_time = map(int, parameters)
            oms.create_order(order_id, system_time, value, delivery_time)
            output_lines.append(f"Order {order_id} has been created - ETA: {system_time + delivery_time}")
        elif action == "printOrder":
            order_id = int(parameters[0])
            oms.print_order(order_id)
        elif action == "printOrdersInTimeRange":
            time1, time2 = map(int, parameters)
            oms.print_orders_in_time_range(time1, time2)
        elif action == "getRankOfOrder":
            order_id = int(parameters[0])
            oms.get_rank_of_order(order_id)
        elif action == "cancelOrder":
            order_id = int(parameters[0])
            oms.cancel_order(order_id)
        elif action == "updateTime":
            order_id, new_delivery_time = int(parameters[0]), int(parameters[1])  # Ensure correct unpacking
            oms.update_time(order_id, new_delivery_time)
    
    # Write output to file
    with open("output_file.txt", 'w') as output_file:
        for line in output_lines:
            output_file.write(line + '\n')


if __name__ == "__main__":
    main()
