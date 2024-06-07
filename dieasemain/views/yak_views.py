import requests
import xml.etree.ElementTree as ET
from flask import Blueprint, url_for, request, render_template, g
from flask import Blueprint, url_for, render_template, abort
from werkzeug.utils import redirect

bp = Blueprint('yak', __name__, url_prefix='/')
totalCount = 0


@bp.route('/yak', methods=['GET', 'POST'])
def list():
    if request.method == 'POST':
        # 검색 폼이 제출되었을 때의 처리
        search_query = request.form['search_query1']
        print(search_query, "=================================")

    else:
        data1 = []
        url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
        pageNo = int(request.args.get('page', 1))
        numOfRows = int(request.args.get('numOfRows', 10))  # 한 페이지에 보여질 항목 수
        params = {
            'serviceKey': 'VQjISU0hGRUuuYzKzUZimCJgNkWsFFAr0VpkfbEIVawBMPCw0FI9aXf0bJ2v1zuDQe45Kupb0ajUCJwjGNQ2cA==',
            'pageNo': pageNo, 'numOfRows': numOfRows, 'entpName': '', 'itemName': '', 'itemSeq': '', 'efcyQesitm': '',
            'useMethodQesitm': '', 'atpnWarnQesitm': '', 'atpnQesitm': '', 'intrcQesitm': '', 'seQesitm': '',
            'depositMethodQesitm': '', 'openDe': '', 'updateDe': '', 'type': 'xml'}
        response = requests.get(url, params=params)

        print(response.status_code)

        if response.status_code == 200:
            # XML 데이터를 파싱합니다
            root = ET.fromstring(response.content)

            try:
                for item in root.findall('.//item'):  # 'item' 태그를 가진 모든 요소를 찾습니다
                    entry = {
                        'itemName': item.find('itemName').text,
                        'itemSeq': item.find('itemSeq').text,  # 상세 정보를 위해 itemSeq를 저장
                        'entpName': item.find('entpName').text,
                        'efcyQesitm': item.find('efcyQesitm').text,
                        'useMethodQesitm': item.find('useMethodQesitm').text,
                        'atpnWarnQesitm': item.find('atpnWarnQesitm').text,
                        'atpnQesitm': item.find('atpnQesitm').text,
                        'intrcQesitm': item.find('intrcQesitm').text,
                        'seQesitm': item.find('seQesitm').text,
                        'depositMethodQesitm': item.find('depositMethodQesitm').text
                    }
                    data1.append(entry)
                totalCount = int(root.find('.//totalCount').text)
                for item in root.findall('.//response'):  # 'item' 태그를 가진 모든 요소를 찾습니다
                    entry1 = {
                        'pageNo': item.find('pageNo').text
                    }
                    data1.append(entry1)

            except ET.ParseError as e:
                print(f"XML 파싱 오류: {e}")
                data1 = []

            total_pages = (totalCount + numOfRows - 1) // numOfRows

    return render_template('yak/list.html', data=data1, totalCount=totalCount, total_pages=total_pages,
                           current_page=pageNo, numOfRows=numOfRows)


# 약품의 세부정보 확인
@bp.route('/yak/<int:itemSeq><itemName>')
def detail(itemSeq, itemName):
    data1 = []
    url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
    pageNo = int(request.args.get('page', 1))
    numOfRows = int(request.args.get('numOfRows', 10))  # 한 페이지에 보여질 항목 수
    params = {
        'serviceKey': 'VQjISU0hGRUuuYzKzUZimCJgNkWsFFAr0VpkfbEIVawBMPCw0FI9aXf0bJ2v1zuDQe45Kupb0ajUCJwjGNQ2cA==',
        'pageNo': pageNo, 'numOfRows': numOfRows, 'entpName': '', 'itemName': itemName, 'itemSeq': '', 'efcyQesitm': '',
        'useMethodQesitm': '', 'atpnWarnQesitm': '', 'atpnQesitm': '', 'intrcQesitm': '', 'seQesitm': '',
        'depositMethodQesitm': '', 'openDe': '', 'updateDe': '', 'type': 'xml'}
    response = requests.get(url, params=params)

    root = ET.fromstring(response.content)

    detail_data = {}
    item = root.find('.//item')
    if item is not None:
        detail_data = {
            'name': item.find('itemName').text,
            'entpName': item.find('entpName').text,
            'efcyQesitm': item.find('efcyQesitm').text,
            'useMethodQesitm': item.find('useMethodQesitm').text,
            'atpnWarnQesitm': item.find('atpnWarnQesitm').text,
            'atpnQesitm': item.find('atpnQesitm').text,
            'intrcQesitm': item.find('intrcQesitm').text,
            'seQesitm': item.find('seQesitm').text,
            'depositMethodQesitm': item.find('depositMethodQesitm').text,
            'itemImage': item.find('itemImage').text
        }
        data1.append(detail_data)
    else:
        print("아이템을 찾을 수 없습니다.")
        abort(404, description="Item not found.")

    return render_template('yak/detail.html', detail_data=detail_data)


# # 약품의 세부정보 확인
# @bp.route('/yak/search')
# def search():
#     detail_data = {}
#     data1 = []
#     # GET 요청으로 받은 검색어 처리
#     search_query = request.args.get('search_query1')
#     print(search_query)
#
#     pageNo = int(request.args.get('page', 1))
#     numOfRows = int(request.args.get('numOfRows', 100))  # 한 페이지에 보여질 항목 수
#     print(search_query)
#     efcyQesitm = search_query
#     # API를 호출하여 검색 결과를 가져옵니다.
#     # 가져온 결과를 템플릿에 전달하여 보여줍니다.
#     url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
#     pageNo = int(request.args.get('page', 1))
#     params = {
#         'serviceKey': 'VQjISU0hGRUuuYzKzUZimCJgNkWsFFAr0VpkfbEIVawBMPCw0FI9aXf0bJ2v1zuDQe45Kupb0ajUCJwjGNQ2cA==',
#         'pageNo': pageNo, 'numOfRows': numOfRows, 'entpName': '', 'itemName': '', 'itemSeq': '', 'efcyQesitm': efcyQesitm,
#         'useMethodQesitm': '', 'atpnWarnQesitm': '', 'atpnQesitm': '', 'intrcQesitm': '', 'seQesitm': '',
#         'depositMethodQesitm': '', 'openDe': '', 'updateDe': '', 'type': 'xml'}
#     response = requests.get(url, params=params)
#
#     root = ET.fromstring(response.content)
#
#     item = root.find('.//item')
#     if item is not None:
#         print(search_query, "=============================================================")
#         detail_data = {
#             'name': item.find('itemName').text,
#             'entpName': item.find('entpName').text,
#             'efcyQesitm': item.find('efcyQesitm').text,
#             'useMethodQesitm': item.find('useMethodQesitm').text,
#             'atpnWarnQesitm': item.find('atpnWarnQesitm').text,
#             'atpnQesitm': item.find('atpnQesitm').text,
#             'intrcQesitm': item.find('intrcQesitm').text,
#             'seQesitm': item.find('seQesitm').text,
#             'depositMethodQesitm': item.find('depositMethodQesitm').text,
#             'itemImage': item.find('itemImage').text
#         }
#         data1.append(detail_data)
#     else:
#         print("아이템을 찾을 수 없습니다.")
#         abort(404, description="Item not found.")
#
#     totalCount = int(root.find('.//totalCount').text)
#     for item in root.findall('.//response'):  # 'item' 태그를 가진 모든 요소를 찾습니다
#         entry1 = {
#             'pageNo': item.find('pageNo').text
#         }
#         data1.append(entry1)
#
#     data1 = []
#
#     total_pages = (totalCount + numOfRows - 1) // numOfRows
#
#     return render_template('yak/search_form.html', detail_data=detail_data,totalCount=totalCount, total_pages=total_pages,
#                            current_page=pageNo, numOfRows=numOfRows)
#


@bp.route('/yak/search')
def search():
    search_query = request.args.get('search_query1', '')
    pageNo = int(request.args.get('page', 1))
    numOfRows = int(request.args.get('numOfRows', 10))

    url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
    params = {
        'serviceKey': 'VQjISU0hGRUuuYzKzUZimCJgNkWsFFAr0VpkfbEIVawBMPCw0FI9aXf0bJ2v1zuDQe45Kupb0ajUCJwjGNQ2cA==',
        'pageNo': pageNo, 'numOfRows': numOfRows, 'entpName': '', 'itemName': '', 'itemSeq': '',
        'efcyQesitm': search_query,  # 검색어를 efcyQesitm에 포함
        'useMethodQesitm': '', 'atpnWarnQesitm': '', 'atpnQesitm': '', 'intrcQesitm': '', 'seQesitm': '',
        'depositMethodQesitm': '', 'openDe': '', 'updateDe': '', 'type': 'xml'}

    response = requests.get(url, params=params)

    data1 = []
    totalCount = 0
    total_pages = 0

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        items = root.findall('.//item')

        if items:
            for item in items:
                efcyQesitm_text = item.find('efcyQesitm').text if item.find('efcyQesitm') is not None else ''
                if search_query in efcyQesitm_text:
                    detail_data = {
                        'name': item.find('itemName').text if item.find('itemName') is not None else 'N/A',
                        'entpName': item.find('entpName').text if item.find('entpName') is not None else 'N/A',
                        'efcyQesitm': item.find('efcyQesitm').text if item.find('efcyQesitm') is not None else 'N/A',
                        'useMethodQesitm': item.find('useMethodQesitm').text if item.find('useMethodQesitm') is not None else 'N/A',
                        'atpnWarnQesitm': item.find('atpnWarnQesitm').text if item.find('atpnWarnQesitm') is not None else 'N/A',
                        'itemImage': item.find('itemImage').text if item.find('itemImage') is not None else 'N/A'
                    }
                    data1.append(detail_data)

            totalCount = int(root.find('.//totalCount').text)
            total_pages = (totalCount + numOfRows - 1) // numOfRows
        else:
            abort(404, description="Item not found.")
    else:
        abort(response.status_code, description="API request failed.")

    return render_template('yak/search_form.html', search_query=search_query, data=data1, totalCount=totalCount, total_pages=total_pages,
                           current_page=pageNo, numOfRows=numOfRows)