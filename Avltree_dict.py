#非再帰の平衡二分木
import copy
class Node:
    """ノード

    Attributes:
        key (any): ノードのキー。比較可能なものであれば良い。(1, 4)などタプルも可。
        val (any): ノードの値。
        lch (Node): 左の子ノード。
        rch (Node): 右の子ノード。
        bias (int): 平衡度。(左部分木の高さ)-(右部分木の高さ)。
        size (int): 自分を根とする部分木の大きさ

    """

    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.lch = None
        self.rch = None
        self.bias = 0
        self.size = 1

class AVLTree:
    """非再帰AVL木

    Attributes:
        root (Node): 根ノード。初期値はNone。
        valdefault (any): ノード値のデフォルト値。デフォルトではNone。（数値、リストなど可）

    """

    def __init__(self,valdefault=None):
        self.root = None
        self.valdefault = valdefault
        
    def rotate_left(self, v):
        u = v.rch
        u.size = v.size
        v.size -= u.rch.size + 1 if u.rch is not None else 1
        v.rch = u.lch
        u.lch = v
        if u.bias == -1:
            u.bias = v.bias = 0
        else:
            u.bias = 1
            v.bias = -1
        return u

    def rotate_right(self, v):
        u = v.lch
        u.size = v.size
        v.size -= u.lch.size + 1 if u.lch is not None else 1
        v.lch = u.rch
        u.rch = v
        if u.bias == 1:
            u.bias = v.bias = 0
        else:
            u.bias = -1
            v.bias = 1
        return u

    def rotateLR(self, v):
        u = v.lch
        t = u.rch
        t.size = v.size
        v.size -= u.size - (t.rch.size if t.rch is not None else 0)
        u.size -= t.rch.size + 1 if t.rch is not None else 1
        u.rch = t.lch
        t.lch = u
        v.lch = t.rch
        t.rch = v
        self.update_bias_double(t)
        return t

    def rotateRL(self, v):
        u = v.rch
        t = u.lch
        t.size = v.size
        v.size -= u.size - (t.lch.size if t.lch is not None else 0)
        u.size -= t.lch.size + 1 if t.lch is not None else 1
        u.lch = t.rch
        t.rch = u
        v.rch = t.lch
        t.lch = v
        self.update_bias_double(t)
        return t

    def update_bias_double(self, v):
        if v.bias == 1:
            v.rch.bias = -1
            v.lch.bias = 0
        elif v.bias == -1:
            v.rch.bias = 0
            v.lch.bias = 1
        else:
            v.rch.bias = 0
            v.lch.bias = 0
        v.bias = 0

    def insert(self, key, val=None):
        """挿入

        指定したkeyを挿入する。valはkeyのノード値。

        Args:
            key (any): キー。
            val (any): 値。（指定しない場合はvaldefaultが入る）

        Note:
            同じキーがあった場合は上書きする。

        """
        if val == None:
            val = copy.deepcopy(self.valdefault)
        if self.root is None:
            self.root = Node(key, val)
            return

        v = self.root
        history = []
        while v is not None:
            if key < v.key:
                history.append((v, 1))
                v = v.lch
            elif v.key < key:
                history.append((v, -1))
                v = v.rch
            elif v.key == key:
                v.val = val
                return

        p, pdir = history[-1]
        if pdir == 1:
            p.lch = Node(key, val)
        else:
            p.rch = Node(key, val)

        while history:
            v, direction = history.pop()
            v.bias += direction
            v.size += 1

            new_v = None
            b = v.bias
            if b == 0:
                break

            if b == 2:
                u = v.lch
                if u.bias == -1:
                    new_v = self.rotateLR(v)
                else:
                    new_v = self.rotate_right(v)
                break
            if b == -2:
                u = v.rch
                if u.bias == 1:
                    new_v = self.rotateRL(v)
                else:
                    new_v = self.rotate_left(v)
                break

        if new_v is not None:
            if len(history) == 0:
                self.root = new_v
                return
            p, pdir = history.pop()
            p.size += 1
            if pdir == 1:
                p.lch = new_v
            else:
                p.rch = new_v

        while history:
            p, pdir = history.pop()
            p.size += 1

    def delete(self, key):
        """削除

        指定したkeyの要素を削除する。

        Args:
            key (any): キー。

        Return:
            bool: 指定したキーが存在するならTrue、しないならFalse。

        """
        v = self.root
        history = []
        while v is not None:
            if key < v.key:
                history.append((v, 1))
                v = v.lch
            elif v.key < key:
                history.append((v, -1))
                v = v.rch
            else:
                break
        else:
            return False

        if v.lch is not None:
            history.append((v, 1))
            lmax = v.lch
            while lmax.rch is not None:
                history.append((lmax, -1))
                lmax = lmax.rch

            v.key = lmax.key
            v.val = lmax.val

            v = lmax

        c = v.rch if v.lch is None else v.lch

        if history:
            p, pdir = history[-1]
            if pdir == 1:
                p.lch = c
            else:
                p.rch = c
        else:
            self.root = c
            return True

        while history:
            new_p = None

            p, pdir = history.pop()
            p.bias -= pdir
            p.size -= 1

            b = p.bias
            if b == 2:
                if p.lch.bias == -1:
                    new_p = self.rotateLR(p)
                else:
                    new_p = self.rotate_right(p)

            elif b == -2:
                if p.rch.bias == 1:
                    new_p = self.rotateRL(p)
                else:
                    new_p = self.rotate_left(p)

            elif b != 0:
                break

            if new_p is not None:
                if len(history) == 0:
                    self.root = new_p
                    return True
                gp, gpdir = history[-1]
                if gpdir == 1:
                    gp.lch = new_p
                else:
                    gp.rch = new_p
                if new_p.bias != 0:
                    break

        while history:
            p, pdir = history.pop()
            p.size -= 1

        return True

    def member(self, key):
        """キーの存在チェック

        指定したkeyがあるかどうか判定する。

        Args:
            key (any): キー。

        Return:
            bool: 指定したキーが存在するならTrue、しないならFalse。

        """
        v = self.root
        while v is not None:
            if key < v.key:
                v = v.lch
            elif v.key < key:
                v = v.rch
            else:
                return True
        return False

    def getval(self, key):
        """値の取り出し

        指定したkeyの値を返す。

        Args:
            key (any): キー。

        Return:
            any: 指定したキーが存在するならそのオブジェクト。存在しなければvaldefault

        """
        v = self.root
        while v is not None:
            if key < v.key:
                v = v.lch
            elif v.key < key:
                v = v.rch
            else:
                return v.val
        self.insert(key)
        return self[key] #

    def lower_bound(self, key):
        """下限つき探索

        指定したkey以上で最小のキーを見つける。[key,inf)で最小

        Args:
            key (any): キーの下限。

        Return:
            any: 条件を満たすようなキー。そのようなキーが一つも存在しないならNone。

        """
        ret = None
        v = self.root
        while v is not None:
            if v.key >= key:
                if ret is None or ret > v.key:
                    ret = v.key
                v = v.lch
            else:
                v = v.rch
        return ret

    def upper_bound(self, key):
        """上限つき探索

        指定したkey未満で最大のキーを見つける。[-inf,key)で最大

        Args:
            key (any): キーの上限。

        Return:
            any: 条件を満たすようなキー。そのようなキーが一つも存在しないならNone。

        """
        ret = None
        v = self.root
        while v is not None:
            if v.key < key:
                if ret is None or ret < v.key:
                    ret = v.key
                v = v.rch
            else:
                v = v.lch
        return ret

    def find_kth_element(self, k):
        """小さい方からk番目の要素を見つける

        Args:
            k (int): 何番目の要素か(0オリジン)。

        Return:
            any: 小さい方からk番目のキーの値。
        """
        v = self.root
        s = 0
        while v is not None:
            t = s+v.lch.size if v.lch is not None else s
            if t == k:
                return v.key
            elif t < k:
                s = t+1
                v = v.rch
            else:
                v = v.lch
        return None
    
    def getmin(self):
        '''
        Return:
            any: 存在するキーの最小値
        '''
        if len(self) == 0:
            raise('empty')
        ret = None
        v = self.root
        while True:
            ret = v
            v = v.lch
            if v == None:
                break
        return ret.key
    
    def getmax(self):
        '''
        Return:
            any: 存在するキーの最大値
        '''
        if len(self) == 0:
            raise('empty')
        ret = None
        v = self.root
        while True:
            ret = v
            v = v.rch
            if v == None:
                break
        return ret.key
    
    def popmin(self):
        '''
        存在するキーの最小値をpopする
        Return:
            any: popした値
        '''
        if len(self) == 0:
            raise('empty')
        ret = None
        v = self.root
        while True:
            ret = v
            v = v.lch
            if v == None:
                break      
        del self[ret.key]
        return ret.key
    
    def popmax(self):
        '''
        存在するキーの最大値をpopする
        Return:
            any: popした値
        '''
        if len(self) == 0:
            raise('empty')
        ret = None
        v = self.root
        while True:
            ret = v
            v = v.rch
            if v == None:
                break
        del self[ret.key]
        return ret.key

    def popkth(self,k):
        '''
        存在するキーの小さい方からk番目をpopする
        Return:
            any: popした値
        '''
        key = self.find_kth_element(k)
        del self[key]
        return key
    
    def get_key_val(self):
        '''
        Return:
            dict: 存在するキーとノード値をdictで出力
        '''
        retdict = dict()
        for i in range(len(self)):
            key = self.find_kth_element(i)
            val = self[key]
            retdict[key] = val
        return retdict
    
    def values(self):
        for i in range(len(self)):
            yield self[self.find_kth_element(i)]

    def keys(self):
        for i in range(len(self)):
            yield self.find_kth_element(i)
    
    def items(self):
        for i in range(len(self)):
            key = self.find_kth_element(i)
            yield key,self[key]

    def __iter__(self): return self.keys()
    def __contains__(self, key): return self.member(key)
    def __getitem__(self, key): return self.getval(key)
    def __setitem__(self, key, val): return self.insert(key, val)
    def __delitem__(self, key): return self.delete(key)
    def __bool__(self): return self.root is not None
    def __len__(self): return self.root.size if self.root is not None else 0


if __name__=='__main__':
    # 普通の平衡二分木としての動作
    AVL = AVLTree()
    AVL.insert(10)
    AVL.insert(20)
    AVL.insert(30)
    AVL.insert(40)
    AVL.insert(50)
    print(AVL.lower_bound(15))
    # 20
    print(AVL.find_kth_element(2))
    # 30
    print(40 in AVL)
    # True
    del AVL[40]   # AVL.delete(40)と等価
    print(40 in AVL)
    # False
    print(list(AVL))
    # [10, 20, 30, 50]
    print(AVL.popmin())
    # 10
    print(AVL.popkth(1)) # 20,30,50のうち1番目(0オリジン)の30
    # 30
    print(list(AVL))
    # [20, 50]
    print(len(AVL))
    # 2

    print()

    AVL1 = AVLTree()
    AVL1['a'] = 'A'
    AVL1['b'] = 'B'
    AVL1['f'] = 'C'
    AVL1['aa'] = 'AA'
    print(list(AVL1))
    # ['a', 'aa', 'b', 'f']
    print(AVL1.get_key_val())
    # {'a': 'A', 'aa': 'AA', 'b': 'B', 'f': 'C'}
    print(AVL1.getmax())
    # f
    print(AVL1.upper_bound('e'))
    # b

    print()

    # defaultdict相当の動作
    AVL2 = AVLTree(valdefault=[])
    AVL2[20].append(2)
    AVL2[20].append(3)
    AVL2[20].append(6)
    AVL2[30].append(5)
    AVL2[40].append(1)
    AVL2[40].append(2)
    print(AVL2.get_key_val())
    # {20: [2, 3, 6], 30: [5], 40: [1, 2]}
    print(AVL2[20].pop())
    # 6
    print(40 in AVL2)
    # True
    print(50 in AVL2)
    # False
    print(AVL2.popmax())
    # 40
    AVL2[50].append(5)
    AVL2[50].append(6)
    print(AVL2.get_key_val())
    # {20: [2, 3], 30: [5], 50: [5, 6]}

    print()

    # Counter相当の動作
    AVL3 = AVLTree(valdefault=0)
    AVL3[30] += 3
    AVL3[40] += 2
    AVL3[50] += 1
    print(AVL3.get_key_val())
    # {30: 3 40: 2, 50: 1}
    AVL3[50] += 5
    print(AVL3.get_key_val())
    # {30: 3, 40: 2, 50: 6}
    print(list(AVL3.values()))
    # [3, 2, 6]
    for key,val in AVL3.items():
        print(key,val)
        # 30 3
        # 40 2
        # 50 6
    while AVL3:
        key = AVL3.getmin()
        print(key,AVL3[key])
        AVL3.popmin()
        # 30 3
        # 40 2
        # 50 6
    