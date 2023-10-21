import datetime
import math


class Obfuscator():

    def __init__(self):
        self.modulo = 1000000000
        self.coprime = 280619659
        self.inverseCoprime = 687208739
        self.digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.maxDigits = 6  # math.ceil(math.log(modulo)/math.log(len(digits)))

    def deobfuscate(self, obfuscated):
        value = 0
        for c in obfuscated:
            value = value * len(self.digits) + self.digits.index(c)
        return (value * self.inverseCoprime % self.modulo)

    def obfuscate(self, original):
        if (original >= self.modulo or original < 0):
            print("out of range")
        value = original * self.coprime % self.modulo
        strbuffer = list(self.digits[:self.maxDigits])
        i = self.maxDigits
        while (value > 0):
            i -= 1
            strbuffer[i] = self.digits[value % len(self.digits)]
            value /= len(self.digits)
            value = int(value)

        while (i > 0):
            i -= 1
            strbuffer[i] = self.digits[0]

        return "".join(strbuffer)


class StringCypher():
    def __init__(self):
        self.digits = "QF8A79JNZG0VEP3S15KOTU4DCYW6H2IRBMLX"
        self.obs = Obfuscator()
        self.obs.digits = self.digits

    def encode(self, clear, key="my JPT 32s@$# key"):
        return self.obs.obfuscate(int(float(clear)))
        # enc = []
        # for i in range(len(clear)):
        #     key_c = key[i % len(key)]
        #     enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        #     enc.append(enc_c)
        # return base64.urlsafe_b64encode("".join(enc).encode()).decode()

    def decode(self, enc, key="my JPT 32s@$# key"):
        return self.obs.deobfuscate(str(enc))
        # dec = []
        # enc = base64.urlsafe_b64decode(enc).decode()
        # for i in range(len(enc)):
        #     key_c = key[i % len(key)]
        #     dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        #     dec.append(dec_c)
        # return "".join(dec)


class Validator():

    def __init__(self):
        self.start_date = datetime.datetime.strptime('Jan 1 2017', '%b %d %Y')
        self.current_date = datetime.datetime.strptime('Jan 1 2017', '%b %d %Y')
        self.password = ""
        self.passwords = ["4XH0-9DSJ-HKGA-CKON", "6XVT-PKMR-RKCP-XH91", "T8Z5-AIVG-MK8G-8DV5", "84M7-S22U-4KEE-YA4A", "TBKR-GUAE-IEYQ-JYKX", "AKPK-897H-EEWE-8RNF", "ZTEW-7KUZ-V0IC-PQQY", "EXMY-GBH8-OEIF-D8XV", "0IEC-NJXT-MKOY-2JSI", "TNRT-AO95-KUUN-P4OJ", "8S2X-7WL0-30A6-22HW", "6UDQ-TUOW-IKIK-9QCK", "UBVV-2B7N-JUON-1XI1", "PCHM-L9LL-C0OP-YIOO", "MC7J-O057-NUIP-EMVV", "SCO6-LMWW-7UM7-GBR0", "DKB4-AHKY-7K2B-ELJD", "2BD8-HIUS-IEKK-VSXD", "IASU-KLHM-1EAU-5BBV", "BJOB-PXWS-IU2G-S87C", "Y7KU-GJFO-D0QP-FJXG", "TCBP-LQIT-NEQL-IQ03", "TTQM-O8RM-SEWO-OQCG", "9AU1-0IKO-BUAJ-CD3U", "0AUX-5TMK-6UY8-XMOC", "LQJM-KN1S-PEAG-GMSM", "6PMT-9KPW-UKYR-PCJT", "39XJ-I9Z7-WUIM-ETOD", "0R7R-GWKZ-2ECD-WBGO", "JGL6-TXIC-8UYA-3S5L", "AOPY-CSOO-DUEQ-PQ8W", "MP5B-FJPI-LKMZ-EIUB", "EKI4-ZWXK-QKOD-MXP8", "SSBO-A774-WUGW-279S", "KUYZ-NJZ6-CKA7-HKTM", "0AX4-UYRJ-LUC9-A5UK", "7EYW-S54E-GU2H-X7XJ", "K1PM-YQ2D-ZUEJ-KCNA", "OT98-X1TS-OKK7-S508", "UWB8-UI7K-MUYX-T5GI", "KGN0-XT8G-DEYM-M5OP", "1KQD-DOBN-MU2I-MEOF", "FMMQ-USLT-SUWC-VFF7", "VTNJ-38UB-FUG4-QGL6", "FTKC-QTHL-IKCT-XBD6", "7DV6-B3ZB-S0WO-7ZTE", "U5OB-AM3R-2KKO-YLKG", "N9TA-USKQ-U0E5-3VG8", "SSFB-EOLC-0U6X-F9LP", "EIPG-FGDV-50S5-YATK", "BRVT-KGM6-QKWU-NSM5", "QXQ6-7VWB-VKCQ-RI78", "UA4O-ZMYP-CK8M-PVHE", "NJKI-WPAK-TUMM-UA8Z", "R9XI-B5OS-FKYQ-E85E", "SK8J-F8NJ-V0M4-VHFL", "IDWZ-6LMV-U0MW-HPTV", "KUZQ-QSXW-00QA-6XIS", "5FLP-OL7C-Y06R-B6C7", "HY8M-2BBI-8KEP-UCM2", "OUA4-3VTQ-FU8C-BR7W", "7RKJ-5TAP-50Q6-FT1U", "UZBW-W3W8-6UQM-QNNI", "VS7R-J5IU-BUWD-IORJ", "GPOT-J43I-N0MC-TDF4", "PGO4-FVHZ-FKSA-QLFR", "NNW8-7P4O-L0G8-COQS", "FBMY-ONE4-1KQN-8IC7", "QN6K-KY7W-7UQL-GEMD", "MALP-GTYH-4K8E-LUIV", "VYGH-BZ8E-OUWE-QALH", "XOZ8-AXJT-OEUT-QCTG", "YTHH-FHGH-8UO9-PBFI", "H76W-61XX-8KAF-ELMQ", "B4L0-3QAA-1UML-AHS7", "V9FD-3QPN-X0GG-SDA9", "KDZF-Z3ZW-Y0C7-NQAH", "0HXD-SEO3-2KMC-1YO5", "7XAQ-EEXY-20U9-DMFS", "XVRV-C1KS-VEO8-CLHD", "IH6A-TXO3-DEMK-MUKU", "PC6F-DTAM-2EAB-8OM4", "F1GM-HBSF-8EOZ-GGMA", "J9L7-DHN8-GK6E-XLL6", "AKKZ-V6EC-30EG-UTPZ", "4MJK-FIXU-ZEIE-4BCT", "ISUU-G1IF-10II-L98P", "CGLR-X7PY-3UWY-GGKJ", "HGUR-P1X5-R0GU-VT7J", "0PN8-SGFP-OKGS-JGDB", "C6NJ-FPDH-8KIX-UA3X", "CBH1-OWJE-S0GG-AFXL", "YPAY-FVWZ-RKSL-JPDE", "S6A7-WBTP-UKWN-9XLI", "POKD-RAFB-XUMX-SCZQ", "3YCM-XMDH-70UM-8KSW", "E8FI-VAB7-908T-9FFK", "6XMC-D3HY-BUCP-U7OD", "B1E8-SXVX-SKAG-VOPC", "LB5Q-WPDH-PE8Z-4NAO" ]
        self.validate()

    def is_valid_password(self, pwd):
        self.password = pwd
        if (len(pwd) == 26):
            time = pwd[-6:]
            pwd = pwd[:19]
            # print(pwd)
            # print(time)
            expiry = Obfuscator().deobfuscate(time)
            # print(expiry)

            if (expiry < 3650):
                expiryDate = self.start_date + datetime.timedelta(days=expiry)
                # print("expiryDate", expiryDate)
                # print("current", current_date)
                if ((pwd in self.passwords) and (expiryDate > self.current_date)):
                    # print("valid")
                    self.write_secret()
                    return True
        return False

    def expired(self):
        print("Product Expired. Please Renew.")
        return False
        # System.Windows.Forms.Application.Exit()
        # this.Close()

    def validated(self):
        print("validated")

    def write_secret(self):
        lines = []
        totDays = math.ceil((datetime.datetime.now() - self.start_date).total_seconds())
        # print("totdays", totDays)
        lines.append(StringCypher().encode(str(totDays)))
        # print(password)
        lines.append(self.password)
        thefile = open('secret.dll', 'w')
        for item in lines:
            thefile.write("%s\n" % item)


    def validate(self):
        with open('secret.dll') as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]

        # print(password)
        try:
            currDays = int(StringCypher().decode(lines[0])) // 86400
            self.password = lines[1]
            # print(password)
        except:
            return self.expired()
        # print(password)
        # print("currdays", currDays)

        if (currDays < (3650) and currDays > 0):
            self.current_date = self.start_date + datetime.timedelta(days=currDays - 1)
            if (self.current_date > datetime.datetime.now()):
                return self.expired()
            else:
                self.write_secret()
                if (self.is_valid_password(self.password)):
                    self.validated()
                else:
                    return self.expired()

        return True


# print(obfuscate(102))
# print((datetime.datetime.now() - start_date).total_seconds())
# print(obfuscate(102))
# print(deobfuscate(obfuscate(102)))
# print(StringCypher().encode('8627584'))
# print(decode('wqTCrFXCgsKA'))
# Validator().validate()
