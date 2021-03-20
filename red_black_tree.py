"""
    Written by  Emil Karlström
                Blekinge Tekniska Högskola
                DVAMI19
    Code for Assignment 2 of course DV1625
    No steal code P L O X 
"""

COLOR_RED = 0
COLOR_BLACK = 1

class RedBlackTree:
    def __init__(self):
        self.root = None
    def insert(self, value):
        nnode = Node(value)
        self._default_binary_tree_insert(nnode)
        if nnode != self.root and nnode.parent:
            self._red_black_tree_fix(nnode)
            self.root.color = COLOR_BLACK
    def _default_binary_tree_insert(self, nnode):
        if self.root:
            node = self.root
            while node:
                if nnode.value < node.value:
                    if node.left:
                        node = node.left
                    else:
                        node.left = nnode
                        nnode.parent = node
                        node = None
                elif nnode.value > node.value:
                    if node.right:
                        node = node.right
                    else:
                        node.right = nnode
                        nnode.parent = node
                        node = None
                else:
                    return
        else:
            self.root = nnode
            self.root.color = COLOR_BLACK
    def _get_uncle(self, node):
        gparent = node.parent.parent
        if gparent:
            if node.parent == gparent.left:
                return gparent.right
            return gparent.left
        return None
    def _red_black_tree_fix(self, nnode):
        uncle = self._get_uncle(nnode)
        uncle_color = uncle.color if uncle else COLOR_BLACK

        gparent = nnode.parent.parent
        parent  = nnode.parent
        
        if parent.color == COLOR_RED:
            if uncle_color == COLOR_RED:
                gparent.color = COLOR_RED
                uncle.color = COLOR_BLACK
                parent.color = COLOR_BLACK
                if gparent.parent:
                    self._red_black_tree_fix(gparent)
            else:
                self._rotate_fix(nnode, uncle, parent, gparent)
    def _rotate_fix(self, nnode, uncle, parent, grandparent):
        if grandparent.right and grandparent.right.left == nnode:
            self._right_rotate(parent)
            self._left_rotate(grandparent)
            nnode.color = COLOR_BLACK
            grandparent.color = COLOR_RED
            parent.color = COLOR_RED
        elif grandparent.right and grandparent.right.right == nnode:
            self._left_rotate(grandparent)
            parent.color = COLOR_BLACK
            grandparent.color = COLOR_RED
            nnode.color = COLOR_RED
        elif grandparent.left and grandparent.left.right == nnode:
            self._left_rotate(parent)
            self._right_rotate(grandparent)
            nnode.color = COLOR_BLACK
            grandparent.color = COLOR_RED
            parent.color = COLOR_RED
        elif grandparent.left and grandparent.left.left == nnode:
            self._right_rotate(grandparent)
            parent.color = COLOR_BLACK
            grandparent.color = COLOR_RED
            nnode.color = COLOR_RED
    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
    def _left_rotate(self, x): # x is the node to rotate around

        y = x.right
        x.right = y.left

        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y
    def _find_node(self, value):
        if not self.root:
            return None
        if value == self.root.value:
            return self.root

        node = self.root
        while node.value != value:
            if value < node.value:
                if node.left:
                    node = node.left
                else:
                    return None
            elif value > node.value:
                if node.right:
                    node = node.right
                else:
                    return None
        return node
    def _successor(self, node):
        succ = node.right
        while succ.left:
            succ = succ.left
        return succ
    def _manage_deletion_case(self, x, x_parent, w=None):
        x_col = COLOR_BLACK if x is None else x.color
        
        # Case 0 check: x is red
        if x_col == COLOR_RED:
            self._deletion_case_0(x)
        else:
            if not w:
                # if x is None: # Special damn cases
                #     x_parent = x_parent.parent
                    # w = x_parent.parent.left if x_parent.parent.left else x_parent.parent.right
                w = x_parent.left if x_parent.right == x else x_parent.right
            # if w is None:
            #     raise RuntimeError(f"w is none, (Parent: {x_parent}) (X: {x})")
            w_col = COLOR_BLACK if w is None else w.color

            # Case 1 check: if the sibling colour is red
            if w_col == COLOR_RED:
                self._deletion_case_1(x, w, x_parent, self._left_rotate if x_parent.left == x else self._right_rotate)
                return
            
            # all cases down below = if the sibling is black

            # Case 2 check: If both children of sibling are black

            if (w.left is None or w.left.color == COLOR_BLACK) and (w.right is None or w.right.color == COLOR_BLACK):
                self._deletion_case_2(x, w, x_parent)
                return

            # all cases down below = at least one child of sibling is red

            # Case 3 check: x is left  child, w.left is red, w.right is black OR
            #               x is right child, w.right is red, w.left is black

            # Case 4 check: x is left  child, w.right is red OR
            #               x is right child, w.left  is red
            if x_parent.left == x:
                # Case 3
                if w.left and w.left.color == COLOR_RED and (w.right is None or w.right.color == COLOR_BLACK):
                    self._deletion_case_3(x, w, x_parent, w.left, self._right_rotate)
                    return
                # Case 4
                if w.right and w.right.color == COLOR_RED:
                    self._deletion_case_4(x, w, x_parent, w.right, self._left_rotate)
                    return
            if x_parent.right == x:
                # Case 3
                if w.right and w.right.color == COLOR_RED and (w.left is None or w.left.color == COLOR_BLACK):
                    self._deletion_case_3(x, w, x_parent, w.right, self._left_rotate)
                    return

                # Case 4
                if w.left and w.left.color == COLOR_RED:
                    self._deletion_case_4(x, w, x_parent, w.left, self._right_rotate)
                    return
            
            # raise RuntimeError(f'NoneType function from _get_deletion_case (No case found)')
    def _deletion_case_0(self, x):
        x.color = COLOR_BLACK
    def _deletion_case_1(self, x, w, x_parent, rotation_function):
        w.color = COLOR_BLACK
        x_parent.color = COLOR_RED
        rotation_function(x_parent)

        if x_parent.left == x:
            w = x_parent.right
        else:
            w = x_parent.left
        self._manage_deletion_case(x, x_parent, w=w)
    def _deletion_case_2(self, x, w, x_parent):
        w.color = COLOR_RED
        x = x_parent
        if x.color == COLOR_RED:
            x.color = COLOR_BLACK
    def _deletion_case_3(self, x, w, x_parent, w_child, rotation_function):
        w_child.color = COLOR_BLACK
        w.color = COLOR_RED
        rotation_function(w)
        w = w.parent

        case_4_child_w = w.left if x_parent.right == x else w.right
        case_4_rotation_function = self._right_rotate if x_parent.right == x else self._left_rotate
        self._deletion_case_4(x, w, x_parent, case_4_child_w, case_4_rotation_function)
    def _deletion_case_4(self, x, w, x_parent, w_child, rotation_function):
        w.color = x_parent.color
        x_parent.color = COLOR_BLACK
        if w_child:
            w_child.color = COLOR_BLACK
        rotation_function(x_parent)
    def remove(self, value):
        node = self._find_node(value)
        if node is None:
            return None
        if node is self.root and not self.root.left and not self.root.right:
            self.root = None
            return

        # Initial steps - How many children
        if node.left is None and node.right is None:  # Two nil children
            replacement = None # x is our replacement
            x = replacement
            x_parent = node.parent
            
            if node.parent.right is node:
                node.parent.right = None
            else:
                node.parent.left = None
        elif node.left is None or node.right is None: # One nil child
            replacement = node.left if node.left else node.right
            x = replacement
            x_parent = node.parent
            
            if node.parent.right is node:
                node.parent.right = x
            else:
                node.parent.left = x
            replacement.parent = node.parent
        else:                                         # No nil children
            replacement = self._successor(node) # successor is our replacement here
            x = replacement.right

            x_parent = replacement.parent
            # Splice out replacement
            if replacement.parent.right == replacement:
                replacement.parent.right = x
            else:
                replacement.parent.left = x
            if x:
                x.parent = replacement.parent
            node.value = replacement.value
        # Initial step 2:
        if node.color == COLOR_RED:
            if replacement and replacement.color == COLOR_BLACK:
                replacement.color == COLOR_RED
                self._manage_deletion_case(x, x_parent)
        else:
            if replacement is None or replacement.color == COLOR_BLACK:
                self._manage_deletion_case(x, x_parent)
            else:
                replacement.color = COLOR_BLACK
    def search(self, value):
        node = self._find_node(value)
        if node:
            return True
        else:
            return False
    def path(self, value):
        path = []
        node = self.root
        found_value = False
        while not found_value:
            path.append(node.value)
            if node.value == value:
                found_value = True
            elif value < node.value:
                if not node.left:
                    return None
                node = node.left
            elif value > node.value:
                if not node.right:
                    return None
                node = node.right
        return path
    def min(self):
        if self.root is None:
            return None
        node = self.root
        while node.left:
            node = node.left
        return node.value
    def max(self):
        if self.root is None:
            return None
        node = self.root
        while node.right:
            node = node.right
        return node.value
    def bfs(self):
        if self.root is None:
            return []
        queue = [ self.root ]
        bfs = []

        while len(queue) > 0:
            node = queue.pop(0)
            bfs.append((
                        node.value,
                        "RED" if node.color == COLOR_RED else "BLACK",
                        node.left.value if node.left else None,
                        node.right.value if node.right else None,
                        ))
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return bfs
class Node:
    def __init__(self, value, parent=None, color=COLOR_RED, left=None, right=None):
        self.value = value
        self.parent = parent
        self.color = color
        self.left = left
        self.right = right