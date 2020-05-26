# ******************************************************************************
class Permutation:

    # ------------------------------------------------------------------------
    @staticmethod
    def get_factoradic(n):
        # --------------------------------------------------------------------
        """
        :arg:
        :return: factoradic:List[int]
        """
        factoradic = [0] * 61
        i = 1
        while n != 0:
            factoradic[61 - i] = int(n % i)
            n = int(n / i)
            i = i + 1
        return factoradic

    # ------------------------------------------------------------------------
    @staticmethod
    def get_unused_char_at_pos(alphabet, pos, used):
        # --------------------------------------------------------------------
        count = -1
        for each in range(0, len(alphabet)):
            if not used[each]:
                count = count + 1
                if count == pos:
                    used[each] = True
                    return alphabet[each]
        return " "

    # ------------------------------------------------------------------------
    def get_permutation(self, alphabet, factoradic):
        # --------------------------------------------------------------------
        perm_in_char = []
        used = [False] * 61  # False list
        for each in factoradic:
            c = self.get_unused_char_at_pos(alphabet, each, used)
            perm_in_char.append(c)
        nth_perm = ''.join(map(str, perm_in_char))
        return nth_perm


def main():
    alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890')  # char list
    total_perms = 5.0758021e+83

    num = total_perms/4
    p = Permutation()
    factoradic = p.get_factoradic(num - 1)  # char list
    res_str = p.get_permutation(alphabet, factoradic)
    print(res_str)


if __name__ == '__main__':
    main()
