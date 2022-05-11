import jaconv
import nfc


class NfcReader:
    def __init__(self, tag):
        self.system_code = None
        self.tag = tag
        self.name_dict = {
            # target : (system_code, service, authority, block)
            "student_number": (0x8c2e, 64, 0x0b, 0),
            "name": (0x8c2e, 64, 0x0b, 1),
        }

    def change_system_code(self, system_code):
        self.system_code = system_code
        idm, pmm = self.tag.polling(system_code=system_code)
        self.tag.idm, self.tag.pmm, self.tag.sys = idm, pmm, system_code

    def read_row(self, target):
        (system_code, service, authrity, block) = self.name_dict[target]

        if self.system_code != system_code:
            self.change_system_code(system_code)

        sc = nfc.tag.tt3.ServiceCode(service, authrity)
        bc = nfc.tag.tt3.BlockCode(block, service=0)
        data = self.tag.read_without_encryption([sc], [bc])
        return data

    def read_name(self):
        name_bytes = self.read_row("name").rstrip(b"\x00")
        half_kana = name_bytes.decode(encoding="shift-jis")
        full_kana = jaconv.h2z(half_kana)
        return full_kana

    def read_student_number(self):
        student_number_bytes = self.read_row("student_number")[2:10]
        student_number = student_number_bytes.decode(encoding="shift-jis")
        return student_number
