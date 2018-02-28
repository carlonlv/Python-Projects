"""
Code for compressing and decompressing using Huffman compression.
Author: Yuan Xu
Dates: 2017-03-20
"""

from nodes import HuffmanNode, ReadNode


# ====================
# Helper functions for manipulating bytes


def get_bit(byte, bit_num):
    """ Return bit number bit_num from right in byte.

    @param int byte: a given byte
    @param int bit_num: a specific bit number within the byte
    @rtype: int

    >>> get_bit(0b00000101, 2)
    1
    >>> get_bit(0b00000101, 1)
    0
    """
    return (byte & (1 << bit_num)) >> bit_num


def byte_to_bits(byte):
    """ Return the representation of a byte as a string of bits.

    @param int byte: a given byte
    @rtype: str

    >>> byte_to_bits(14)
    '00001110'
    """
    return "".join([str(get_bit(byte, bit_num))
                    for bit_num in range(7, -1, -1)])


def bits_to_byte(bits):
    """ Return int represented by bits, padded on right.

    @param str bits: a string representation of some bits
    @rtype: int

    >>> bits_to_byte("00000101")
    5
    >>> bits_to_byte("101") == 0b10100000
    True
    """
    return sum([int(bits[pos]) << (7 - pos)
                for pos in range(len(bits))])


# ====================
# Functions for compression


def make_freq_dict(text):
    """ Return a dictionary that maps each byte in text to its frequency.

    @param bytes text: a bytes object
    @rtype: dict{int,int}

    >>> d = make_freq_dict(bytes([65, 66, 67, 66]))
    >>> d == {65: 1, 66: 2, 67: 1}
    True
    """
    freq_dict = {}
    for i in text:
        if i in freq_dict:
            freq_dict[i] += 1
        else:
            freq_dict[i] = 1
    return freq_dict


def huffman_tree(freq_dict):
    """ Return the root HuffmanNode of a Huffman tree corresponding
    to frequency dictionary freq_dict.

    @param dict(int,int) freq_dict: a frequency dictionary
    @rtype: HuffmanNode

    >>> freq = {2: 6, 3: 4}
    >>> t = huffman_tree(freq)
    >>> result1 = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> result2 = HuffmanNode(None, HuffmanNode(2), HuffmanNode(3))
    >>> t == result1 or t == result2
    True
    >>> freq = {3:10, 5:20, 7:30, 11:40, 13:50}
    >>> huffman_tree(freq)

    """
    # Create a list of tuple(freq, HuffmanNode) and sorted by freq
    lst = []
    for key in freq_dict:
        lst.append((freq_dict[key], HuffmanNode(key)))
    lst.sort()
    # Create huffman tree
    while len(lst) > 1:
        first = lst.pop(0)
        second = lst.pop(0)
        new_freq = first[0] + second[0]
        new_node = HuffmanNode(None, first[1], second[1])
        lst.append((new_freq, new_node))
        lst.sort()
    return lst[0][1]

def get_codes(tree):
    """ Return a dict mapping symbols from tree rooted at HuffmanNode to codes.

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @rtype: dict(int,str)

    >>> tree = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> d = get_codes(tree)
    >>> d == {3: "0", 2: "1"}
    True
    """
    # base case leaf
    d = {}
    if not tree:
        return {}
    if tree.is_leaf():
        d = {tree.symbol: ""}
    # recursion internal
    for key, value in get_codes(tree.left).items():
        d[key] = "0" + value
    for key, value in get_codes(tree.right).items():
        d[key] = "1" + value
    return d


def number_nodes(tree):
    """ Number internal nodes in tree according to postorder traversal;
    start numbering at 0.

    @param HuffmanNode tree:  a Huffman tree rooted at node 'tree'
    @rtype: NoneType

    >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> right = HuffmanNode(None, HuffmanNode(9), HuffmanNode(10))
    >>> tree = HuffmanNode(None, left, right)
    >>> number_nodes(tree)
    >>> tree.left.number
    0
    >>> tree.right.number
    1
    >>> tree.number
    2
    """
    def helper(t, num):
        """Number internal nodes in t according to postorder traversal:
         start numbering at num and return the next num

        @param HuffmanNode t:  a Huffman tree rooted at node 'tree'
        @param int num:  starting number
        @rtype: int

        >>> tree = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
        >>> helper(tree, 0)
        1
        """
        if t.is_leaf():
            return num
        num = helper(t.left, num)
        num = helper(t.right, num)
        if t.symbol is None:
            t.number = num
            return num + 1
        return num

    helper(tree, 0)


def avg_length(tree, freq_dict):
    """ Return the number of bits per symbol required to compress text
    made of the symbols and frequencies in freq_dict, using the Huffman tree.

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @param dict(int,int) freq_dict: frequency dictionary
    @rtype: float

    >>> freq = {3: 2, 2: 7, 9: 1}
    >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> right = HuffmanNode(9)
    >>> tree = HuffmanNode(None, left, right)
    >>> avg_length(tree, freq)
    1.9
    """
    # get total number of frequency
    total_number = sum(freq_dict.values())
    # get total number of bits
    dict_ = get_codes(tree)
    number_of_bits = 0
    for key in freq_dict:
        number_of_bits += len(dict_[key]) * (freq_dict[key])
    # calculate
    return number_of_bits / total_number


def generate_compressed(text, codes):
    """ Return compressed form of text, using mapping in codes for each symbol.

    @param bytes text: a bytes object
    @param dict(int,str) codes: mappings from symbols to codes
    @rtype: bytes

    >>> d = {0: "0", 1: "10", 2: "11"}
    >>> text = bytes([1, 2, 1, 0])
    >>> result = generate_compressed(text, d)
    >>> [byte_to_bits(byte) for byte in result]
    ['10111000']
    >>> text = bytes([1, 2, 1, 0, 2])
    >>> result = generate_compressed(text, d)
    >>> [byte_to_bits(byte) for byte in result]
    ['10111001', '10000000']
    """
    # get codes
    result = []
    temp = ""
    for i in text:
        temp += codes.get(i, "")
    # complement
    while len(temp) % 8 != 0:
        temp += "0"
    # take byte into list
    for i in range(0, len(temp), 8):
        result.append(bits_to_byte(temp[i: i + 8]))
    return bytes(result)


def tree_to_bytes(tree):
    """ Return a bytes representation of the tree rooted at tree.

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @rtype: bytes

    The representation should be based on the postorder traversal of tree
    internal nodes, starting from 0.
    Precondition: tree has its nodes numbered.

    >>> tree = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2]
    >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> right = HuffmanNode(5)
    >>> tree = HuffmanNode(None, left, right)
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2, 1, 0, 0, 5]
    """
    lst_bytes = []
    if not (tree.left is None and tree.right is None):
        lst_bytes.extend(tree_to_bytes(tree.left))
        lst_bytes.extend(tree_to_bytes(tree.right))
        if tree.left.is_leaf():
            lst_bytes.extend([0, tree.left.symbol])
        if not tree.left.is_leaf():
            lst_bytes.extend([1, tree.left.number])
        if tree.right.is_leaf():
            lst_bytes.extend([0, tree.right.symbol])
        if not tree.right.is_leaf():
            lst_bytes.extend([1, tree.right.number])
    return bytes(lst_bytes)


def num_nodes_to_bytes(tree):
    """ Return number of nodes required to represent tree (the root of a
    numbered Huffman tree).

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @rtype: bytes
    """
    return bytes([tree.number + 1])


def size_to_bytes(size):
    """ Return the size as a bytes object.

    @param int size: a 32-bit integer that we want to convert to bytes
    @rtype: bytes

    >>> list(size_to_bytes(300))
    [44, 1, 0, 0]
    """
    # little-endian representation of 32-bit (4-byte)
    # int size
    return size.to_bytes(4, "little")


def compress(in_file, out_file):
    """ Compress contents of in_file and store results in out_file.

    @param str in_file: input file whose contents we want to compress
    @param str out_file: output file, where we store our compressed result
    @rtype: NoneType
    """
    with open(in_file, "rb") as f1:
        text = f1.read()
    freq = make_freq_dict(text)
    tree = huffman_tree(freq)
    codes = get_codes(tree)
    number_nodes(tree)
    print("Bits per symbol:", avg_length(tree, freq))
    result = (num_nodes_to_bytes(tree) + tree_to_bytes(tree) +
              size_to_bytes(len(text)))
    result += generate_compressed(text, codes)
    with open(out_file, "wb") as f2:
        f2.write(result)


# ====================
# Functions for decompression


def generate_tree_general(node_lst, root_index):
    """ Return the root of the Huffman tree corresponding
    to node_lst[root_index].

    The function assumes nothing about the order of the nodes in the list.

    @param list[ReadNode] node_lst: a list of ReadNode objects
    @param int root_index: index in the node list
    @rtype: HuffmanNode

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 1, 1, 0)]
    >>> generate_tree_general(lst, 2)
    HuffmanNode(None, HuffmanNode(None, HuffmanNode(10, None, None), \
HuffmanNode(12, None, None)), \
HuffmanNode(None, HuffmanNode(5, None, None), HuffmanNode(7, None, None)))
    """
    tree = HuffmanNode()
    root_node = node_lst[root_index]
    if root_node.l_type == 0:
        tree.left = HuffmanNode(root_node.l_data)
    else:
        tree.left = generate_tree_general(node_lst, root_node.l_data)
    if root_node.r_type == 0:
        tree.right = HuffmanNode(root_node.r_data)
    else:
        tree.right = generate_tree_general(node_lst, root_node.r_data)
    return tree


def generate_tree_postorder(node_lst, root_index):
    """ Return the root of the Huffman tree corresponding
    to node_lst[root_index].

    The function assumes that the list represents a tree in postorder.

    @param list[ReadNode] node_lst: a list of ReadNode objects
    @param int root_index: index in the node list
    @rtype: HuffmanNode

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 0, 1, 0)]
    >>> generate_tree_postorder(lst, 2)
    >>> L = [ReadNode(0,3,0,7), ReadNode(0,2,0,5), ReadNode(1,0,1,1)]
    >>> generate_tree_postorder(L, 2)

    HuffmanNode(None, HuffmanNode(None, HuffmanNode(5, None, None), \
HuffmanNode(7, None, None)), \
HuffmanNode(None, HuffmanNode(10, None, None), HuffmanNode(12, None, None)))
    """

    def count_internal(t):
        """Return the number of internal nodes of t.
        @param Tree t: tree to list internal values of
        @rtype: int

        >>> tree = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
        >>> count_internal(tree)
        1
        """
        if not t:
            return 0
        acc = 0
        if not t.is_leaf():
            acc += 1
        for c in [t.left, t.right]:
            acc += count_internal(c)
        return acc

    tree = HuffmanNode()
    tree.number = root_index
    root_node = node_lst[root_index]
    if root_node.r_type == 0:
        tree.right = HuffmanNode(root_node.r_data)
    else:
        root_index -= 1
        tree.right = generate_tree_general(node_lst, root_index)
    if root_node.l_type == 0:
        tree.left = HuffmanNode(root_node.l_data)
    else:
        root_index -= count_internal(tree.right)
        tree.left = generate_tree_general(node_lst, root_index)
    return tree


def generate_uncompressed(tree, text, size):
    """ Use Huffman tree to decompress size bytes from text.

    @param HuffmanNode tree: a HuffmanNode tree rooted at 'tree'
    @param bytes text: text to decompress
    @param int size: how many bytes to decompress from text.
    @rtype: bytes
    """
    # get code from tree and create a dict{code: symbol}
    codes = get_codes(tree)
    d = {}
    for key, value in codes.items():
        d[value] = key
    # get string with all bits
    temp = ""
    for byte in text:
        temp += byte_to_bits(byte)
    # find byte corresponding to bits
    result = []
    current = ""
    index = 0
    count = 0
    while count < size:
        current += temp[index]
        if current in d:
            result.append(d[current])
            current = ""
            count += 1
        index += 1
    return bytes(result)


def bytes_to_nodes(buf):
    """ Return a list of ReadNodes corresponding to the bytes in buf.

    @param bytes buf: a bytes object
    @rtype: list[ReadNode]

    >>> bytes_to_nodes(bytes([0, 1, 0, 2]))
    [ReadNode(0, 1, 0, 2)]
    """
    lst = []
    for i in range(0, len(buf), 4):
        l_type = buf[i]
        l_data = buf[i+1]
        r_type = buf[i+2]
        r_data = buf[i+3]
        lst.append(ReadNode(l_type, l_data, r_type, r_data))
    return lst


def bytes_to_size(buf):
    """ Return the size corresponding to the
    given 4-byte little-endian representation.

    @param bytes buf: a bytes object
    @rtype: int

    >>> bytes_to_size(bytes([44, 1, 0, 0]))
    300
    """
    return int.from_bytes(buf, "little")


def uncompress(in_file, out_file):
    """ Uncompress contents of in_file and store results in out_file.

    @param str in_file: input file to uncompress
    @param str out_file: output file that will hold the uncompressed results
    @rtype: NoneType
    """
    with open(in_file, "rb") as f:
        num_nodes = f.read(1)[0]
        buf = f.read(num_nodes * 4)
        node_lst = bytes_to_nodes(buf)
        # use generate_tree_general or generate_tree_postorder here
        tree = generate_tree_general(node_lst, num_nodes - 1)
        size = bytes_to_size(f.read(4))
        with open(out_file, "wb") as g:
            text = f.read()
            g.write(generate_uncompressed(tree, text, size))


# ====================
# Other functions

def improve_tree(tree, freq_dict):
    """ Improve the tree as much as possible, without changing its shape,
    by swapping nodes. The improvements are with respect to freq_dict.

    @param HuffmanNode tree: Huffman tree rooted at 'tree'
    @param dict(int,int) freq_dict: frequency dictionary
    @rtype: NoneType

    >>> left = HuffmanNode(None, HuffmanNode(99), HuffmanNode(100))
    >>> right = HuffmanNode(None, HuffmanNode(101), \
    HuffmanNode(None, HuffmanNode(97), HuffmanNode(98)))
    >>> tree = HuffmanNode(None, left, right)
    >>> freq = {97: 26, 98: 23, 99: 20, 100: 16, 101: 15}
    >>> improve_tree(tree, freq)
    >>> avg_length(tree, freq)
    2.31
    """
    # get list(frequency, symbol) from high frequency to low frequency
    lst = []
    for key, value in freq_dict.items():
        lst.append((value, key))
    lst.sort(reverse=True)
    # levelorder visited and change symbol of leaf
    nodes = [tree]
    while len(nodes) != 0:
        next_node = nodes.pop(0)
        if next_node.is_leaf():
            next_node.symbol = lst.pop(0)[1]
        if next_node.left:
            nodes.append(next_node.left)
        if next_node.right:
            nodes.append(next_node.right)


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config="huffman_pyta.txt")
    import doctest
    doctest.testmod()

    import time

    mode = input("Press c to compress or u to uncompress: ")
    if mode == "c":
        fname = input("File to compress: ")
        start = time.time()
        compress(fname, fname + ".huf")
        print("compressed {} in {} seconds."
              .format(fname, time.time() - start))
    elif mode == "u":
        fname = input("File to uncompress: ")
        start = time.time()
        uncompress(fname, fname + ".orig")
        print("uncompressed {} in {} seconds."
              .format(fname, time.time() - start))
