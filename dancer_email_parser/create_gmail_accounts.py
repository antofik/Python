import httplib
import urllib
import zlib

__author__ = 'anton'

def main():
    data = post_page(2)
    print data

def post_page(number):
    host = 'www.google.com'
    url = '/a/cpanel/mfst.pro/Organization/CreateUser'
    connection = httplib.HTTPConnection(host)
    params = {
    'firstName':'noreply',
    'lastName':'noreply',
    'userDomain':'mfst.pro',
    'userName':'noreply%s' % number,
    'password.newPassword.alpha':'noreply$$$',
    'password.newPassword.beta':'noreply$$$',
    'email':'noreply%s@mfst.pro' % number,
    'password.isSet':'true',
    'maskedOrgUnitId':'3b3herm3q4jy2h',
    'passwordStrength':'3',
    'userListSortField':'EMAIL',
    'userListSortAscending':'true',
    'userListRowCount':'30',
    'uninviteAction':'false',
    'conflictAction':'ASK',
    'defalultConflictAction':'false',
    }

    params = urllib.urlencode(params)
    cookie = 'CP_AT=UZWLxI1lzsKliMkCkd4XQfV1dXI; CPH_SID=DQAAAPYAAACevkID6pzp8-VeG93316X9VLLaGHwcIcQcqDLc8mliRJLGfqCmqNYC9LSYTMZgOv5vlS8QaykUGZvrWN1PZuAd6NDkB07-mwmL5uLE2SujXKErAIj3p7JYG3niL4hxctwH_HNr4jAQrbcRi5oMBpUqa89dccLsV-jm_yicdfoVz5bN6c0uVj4lOXcXufboEpICCMLsxwuZtBZ0299aK-TWK2D1tvaeq4HpzqaRk_8x52GEn62UHWZzFPSoQ1tWg6pGFQWDaXvb3QH5IyNaMCQpF3yOV_C3cf_zzB-7Q3gBenQphcNsigXcONM4w52wcwqHvo9ZCLtdSoAwnYn8O0AI; GoogleAccountsLocale_session=ru; __utma=173272373.1382311079.1346845617.1346845617.1346845617.1; __utmb=173272373.7.10.1346845617; __utmc=173272373; __utmz=173272373.1346845617.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); NID=63=FGBbR_DywRpNoKN7Y8blYJUdGM67p8xiSGoF64h3hoyBiAMeRnswA7YCrci0AiHKw43D8Lt4jxIRZGE2k3SM-qBsf1WZ7g7D2ENTmTagBFIKjZyRPwCHi01xWqjo0F3dR1LrOQ; HSID=AYa-jbjXp3RGsmnML; SSID=AOCQ0cwYIGSFhkSF_; APISID=vyhl_fxZVs3fMFFk/AM7sDxDZvl4fuopr4; SAPISID=4sfyT0wqtfwQV5OZ/AdEqpM8olXN4PH2kd; PREF=ID=a7a46c3459f1a458:FF=0:LD=ru:TM=1346845540:LM=1346845540:GM=1:S=SMtk9rc59zHCsyAR; SID=DQAAAPUAAADvgU_PEppcFR5HdpM0gcX3JOtRUWBR-iaLbd5BOnU02OiCgEixtSa6SgYWMq-bQW0k_vIpVvo9DAe_dAkLYQmeQuTiuJ6jcOyXkCIeBtANt2CF3aXq5i0Y_3Xd8j9aj40dFJKD3fFKa4GgExjMK-12K8--8cqb2YmXG4lWYHDatJ_c4H7yAahMWHtnYwGqYhyaNL0QlPJI22VD_eIFQk7AEcq_-Mjsxuw_vKdQeXokIuy0lRl8usr6Zh35jEjGUDzXYAT3DeqyjjgERQ7FgWXlZ-CWAz_1lIPtttJeQ92TVj_TgsCBHtpIKl0aUwSPyHog6csNPVzylH4qRpSVkCG6'
    headers = {
        "Content-type": "application/x-www-form-urlencoded; charset=utf-8",
        'Accept-Encoding':'deflate, gzip',
        'Cookie':cookie,
        'Accept':'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1',
        'X-DCP-XsrfToken':	'DEHwauCZnRBZTrTvQV_iTek58_E:1346845617613',
        'X-DCP-GwtRpcRefererUrl':	'https://www.google.com/a/cpanel/mfst.pro/ServiceSettings#Organization',
    }
    connection.request('POST', url, params, headers)
    response = connection.getresponse()
    print response.msg
    data = response.read()
    try:
        data = zlib.decompress(data)
        data = data.decode('cp1251').encode('utf8')
    except Exception, ex:
        print ex
    return data


if __name__=="__main__":
    main()