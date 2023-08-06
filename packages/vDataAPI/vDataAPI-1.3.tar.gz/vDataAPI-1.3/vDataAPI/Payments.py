from requests import post,get
from requests.exceptions import HTTPError


class VDataPayments:
    def __init__(self, callbackURI, redirectURI, apikey):
        """
        Set variables for functions

        :param callbackURI: URL to send request by API after pay
        :param redirectURI: URL to redirect user after payment
        :param apikey: APIKey generated in dash.vdata.pl
        """
        if not callbackURI or not redirectURI or not apikey:
            raise Exception("[ HSCode ] callbackURI, redirectURI and apikey is required!")
        else:
            self.callbackURI = callbackURI
            self.redirectURI = redirectURI
            self.apikey = apikey
            self.baseURL = "https://api.vdata.pl/v1/"

    def generate_payment(self, amount):
        """
        Generate payment for user

        :param amount: Amount of cash to pay for user account
        :return:
        """

        if not amount:
            raise Exception("[ HSCode ] Amount is required!")

        try:
            apirequest = post(self.baseURL + "payment/generate", data={
                "amount": amount,
                "contiuneUrl": self.redirectURI,
                "webhookUrl": self.callbackURI
            }, headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.apikey}"
            })

            return apirequest.json()
        except HTTPError as e:
            raise Exception("[ HSCode ] Error with processing request\n{}".format(e))

    def check_payment_status(self, paymentid):
        """
        Getting information about payment

        :param paymentID: ID of payment to check
        :return:
        """

        if not paymentid:
            raise Exception("[ HSCode ] paymentid is required!")

        try:
            apirequest = get(self.baseURL + "payment/verify?paymentId={}".format(paymentid), headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.apikey}"
            })

            return apirequest.json()
        except HTTPError as e:
            raise Exception("[ HSCode ] Error with processing request\n{}".format(e))
