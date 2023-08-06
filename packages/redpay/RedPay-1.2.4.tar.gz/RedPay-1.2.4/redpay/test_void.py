
import json

from redpay import RedPay

if __name__ == "__main__":
    redpay = RedPay("DEMO",
                    "MIIBojANBgkqhkiG9w0BAQEFAAOCAY8AMIIBigKCAYEAtsQxNp3vmKVNYIxfWSi0LIRgCnPaMn0MUNouxgrs4zmg4cnvSeQ3I8YP03YbpXuWA80RvOw/nWErYAKomniJw8Y+xexMfBQ5sgJgewn3ZnRPNM9Y4Z62gwfIlsrs7Bwvpz9uUtLgeQLl1ffNaumnu1IBrqRps0EZ1QyDuu41UckTyo31C40Wez6IbeMfZeusrmPlIWqyBacdviJ5zHCA3zHNq86QMnB8HOP1U81HOSs6GTTelhD7lCoJ+fHKHxcz0MDr37fNpKpC57B0/20wBXFp9tlVtSkHcIty1lyNk2/HDH8knCdqkZk+fCvWgGwdex41x8/rM+LKC13c5J/yG6Gb2PnKhwNk4lvvnz73YAdqTUJ7qNrdtWVnOTWfbMBiNlpBCVqt8xY8UK6u83AVWrWXse0xe2Pn/kRqlXmxWT0mGEoCavjvZ9lQUL7LXAXZ1dff9r+oFUZo6xDQ3ER/OTIKa4jpvaI9S/J1drsrI1f9kkMWFwEh48dCPYplGSxzAgMBAAE=",
                    "redpaystable.azurewebsites.net")

    request = {
        "transactionId": "DEMO.gu377jz1r98e5zfc"
    }

    print("VOID request >>>")
    print(json.dumps(request, indent=2))

    response = redpay.Void(request)

    print("VOID response >>>")
    print(json.dumps(response, indent=2))
