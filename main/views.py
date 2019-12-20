import re

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Case, When, IntegerField
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from main.models import SungWonList, SungWonSettings


def index(request):
    small = SungWonSettings.objects.get(key_name='s')
    medium = SungWonSettings.objects.get(key_name='m')
    large = SungWonSettings.objects.get(key_name='l')

    lists = SungWonList.objects.filter(Q(flag='y', price__lte=small.price, size=59) | Q(flag='y', price__lte=medium.price, size=84) | Q(flag='y', price__lte=large.price, size=133))[:5]

    # 부동산별 매물갯수 현황
    each_office = SungWonList.objects.all().values('office').annotate(
        count=Count('pk', distinct=True),
        count_now=Count(Case(
            When(flag='y', then=1),
            output_field=IntegerField(),
        ))
    ).order_by('-count_now')
    print(each_office)

    context = {
        'lists' : lists,
        'sm' : small,
        'md' : medium,
        'lg' : large,
        'each_office': each_office
    }

    return render(request, 'main/index.html', context)


def pre_cron(request):
    import requests
    import json
    import logging


    URL = "https://m.land.naver.com/complex/getComplexArticleList"

    param = {
        'hscpNo': '2221',
        'tradTpCd': 'A1',
        'order': 'date_',
        'showR0': 'N',
    }

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
        'Referer': 'https://m.land.naver.com/'
    }

    page = 0

    SungWonList.objects.update(flag="n")

    while True:
        page += 1
        param['page'] = page

        resp = requests.get(URL, params=param, headers=header)
        if resp.status_code != 200:
            print('invalid status: %d' % resp.status_code)
            break

        data = json.loads(resp.text)
        result = data['result']
        if result is None:
            print('no result')
            break

        for item in result['list']:
            if not SungWonList.objects.filter(article_num=int(item['atclNo'])).exists():
                print('생성합니다')
                price_re = re.findall(r'[0-9]+', item['prcInfo'])
                price_all = ""
                if len(price_re) is 3:
                    for i in price_re:
                        price_all += i

                elif len(price_re) is 2:
                    price_re.insert(1, '0')

                    for i in price_re:
                        price_all += i

                elif len(price_re) is 1:
                    price_re.insert(1, '0')
                    price_re.insert(2, '000')

                    for i in price_re:
                        price_all += i

                else:
                    pass

                creating = SungWonList.objects.create(
                    article_num=int(item['atclNo']),
                    size=float(item['spc2']),
                    dong=item['bildNm'],
                    where=item['flrInfo'],
                    office=item['rltrNm'],
                    owner=item['vrfcTpCd'],
                    trade=item['tradCmplYn'],
                    price=price_all
                )
                creating.save()

            elif SungWonList.objects.filter(article_num=int(item['atclNo'])).exists():
                print('update 합니다')
                SungWonList.objects.filter(article_num=int(item['atclNo'])).update(
                    flag='y',
                    trade=item['tradCmplYn']
                )



                # if 58 < float(item['spc2']) < 60 and int(price_all) <= small.price:
                #     creating = SungWonList.objects.create(
                #         article_num=int(item['atclNo']),
                #         size=float(item['spc2']),
                #         dong=item['bildNm'],
                #         where=item['flrInfo'],
                #         office=item['rltrNm'],
                #         price=price_all
                #     )
                #     creating.save()
                # elif 84 < float(item['spc2']) < 85 and int(price_all) <= medium.price:
                #     creating = SungWonList.objects.create(
                #         article_num=int(item['atclNo']),
                #         size=float(item['spc2']),
                #         dong=item['bildNm'],
                #         where=item['flrInfo'],
                #         office=item['rltrNm'],
                #         price=price_all
                #     )
                #     creating.save()
                # elif 133 < float(item['spc2']) < 134 and int(price_all) <= large.price:
                #     creating = SungWonList.objects.create(
                #         article_num=int(item['atclNo']),
                #         size=float(item['spc2']),
                #         dong=item['bildNm'],
                #         where=item['flrInfo'],
                #         office=item['rltrNm'],
                #         price=price_all
                #     )
                #     creating.save()
                # else:
                #     pass

            else:
                pass
        if result['moreDataYn'] == 'N':
            break

    return render(request, 'main/index.html')


def fake_list(request):
    small = SungWonSettings.objects.get(key_name='s')
    medium = SungWonSettings.objects.get(key_name='m')
    large = SungWonSettings.objects.get(key_name='l')
    lists = SungWonList.objects.filter(
        Q(flag='y', price__lte=small.price, size=59) |
        Q(flag='y', price__lte=medium.price, size=84) |
        Q(flag='y', price__lte=large.price, size=133)
    )

    context = {
        'lists' : lists
    }

    return render(request, 'main/fake_list.html', context)


def fake_list_all(request):
    small = SungWonSettings.objects.get(key_name='s')
    medium = SungWonSettings.objects.get(key_name='m')
    large = SungWonSettings.objects.get(key_name='l')
    lists = SungWonList.objects.filter(
        Q(flag='y', price__lte=small.price, size=59) |
        Q(flag='y', price__lte=medium.price, size=84) |
        Q(flag='y', price__lte=large.price, size=133)
    )

    context = {
        'lists' : lists
    }

    return render(request, 'main/fake_list_all.html', context)




@login_required
def change_to_doctor_status_ajax(request):
    if request.is_ajax():
        get_pk = request.POST.get('target')
        if SungWonList.objects.filter(article_num=get_pk).exists():
            apart = SungWonList.objects.get(article_num=get_pk)
            apart.members.add(request.user)

        else:
            print("해당매물이 존재하지 않습니다")

        context = {
            'ok': 'ok'
        }
        return JsonResponse(context)


@login_required
def change_back_singo_ajax(request):
    if request.is_ajax():
        get_pk = request.POST.get('target')
        if SungWonList.objects.filter(article_num=get_pk).exists():
            apart = SungWonList.objects.get(article_num=get_pk)
            apart.members.remove(request.user)

        else:
            print("해당매물이 존재하지 않습니다")

        context = {
            'ok': 'ok'
        }
        return JsonResponse(context)


class AllApartListsView(ListView):
    model = SungWonList
    paginate_by = 2
    context_object_name = 'lists'
    template_name = 'main/all_apart_lists.html'
    ordering = ['-article_num']


all_apart_lists = AllApartListsView.as_view()

