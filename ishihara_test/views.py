import json
import threading
import uuid
from django.contrib import messages

from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .models import UserInfo, IshiharaTest
from .forms import ContactForm
from django.db import transaction
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def home_view(request):
    return render(request, 'home.html')


def test_view(request, test_type):
    context = {
        'test_type': test_type,
    }
    return render(request, 'test.html', context)


def submit_test(request):
    if request.method == 'POST':
        print(request.body)
        if not request.body:
            return JsonResponse({"status": "error", "error": "No data provided."})
        data = json.loads(request.body.decode('utf-8'))
        with transaction.atomic():
            phone = data['user_info']['phone']
            test_type = data['test_type']
            if phone and UserInfo.objects.filter(phone=phone).exists():
                if test_type and UserInfo.objects.filter(phone=phone, test_type=test_type).exists():
                    return JsonResponse({"status": "error", "error": "이미 참여한 전화번호입니다."})
                token = UserInfo.objects.get(phone=phone).token
                share_count = UserInfo.objects.get(phone=phone).share_count
                data['user_info']['token'] = token
                data['user_info']['share_count'] = share_count
            user = UserInfo.objects.create(
                **data['user_info'],
                test_type=data['test_type'],
            )
            test = IshiharaTest.objects.create(
                user=user,
                responses=data['responses'],
                score=data['score'],
                cvd_type=data['cvd_type'],
            )
            if not user or not test:
                return JsonResponse({"status": "error", "error": "데이터를 저장하는 데 실패하였습니다. 다시 시도해 주세요."})
            token = request.session.get('share_token')
            if token:
                try:
                    share_users = UserInfo.objects.filter(token=token)
                    for share_user in share_users:
                        share_user.share_count += 1
                        share_user.save()
                except UserInfo.DoesNotExist:
                    pass
            context = {
                'score': test.score,
                'result_url': request.build_absolute_uri(reverse('results', kwargs={'uuid': user.uuid})),
                'submitted_at': test.submitted_at,
                'share_url': request.build_absolute_uri(reverse('share', kwargs={'token': user.token})),
                'test_type': "간편" if test_type == 'short' else "정밀",
                'cvd_score': '없음' if test.score <= 15 else '보통' if test.score <= 40 else '높음' if test.score <= 65 else '매우 높음',
            }
            threading.Thread(target=send_email, args=(user.email, test_type, context)).start()
            messages.success(request, f'검사 결과가 성공적으로 저장되었습니다. {user.email}로 결과를 전송하였습니다.')
            return JsonResponse({"status": "success", "uuid": str(user.uuid)})
    return HttpResponseBadRequest()


def send_email(user_email, test_type, context):
    html_content = render_to_string('email_result_card.html', context)
    subject = f"제1·2종 색각 이상 검사 결과 ({'간편' if test_type == 'short' else '정밀'})"
    from_email = 'gshs.ishihara@gmail.com'
    recipient_list = [user_email]
    email = EmailMessage(subject, html_content, from_email, recipient_list)
    email.content_subtype = "html"
    email.send()


def show_results(request, uuid):
    if uuid:
        try:
            user = UserInfo.objects.get(uuid=uuid)
            test = IshiharaTest.objects.get(user=user)
            return render(request, 'results.html', {'user': user, 'test': test})
        except UserInfo.DoesNotExist:
            messages.error(request, '결과를 조회할 수 없습니다.')
            return redirect('home')
    return redirect('home')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '문의사항이 성공적으로 전송되었습니다.')
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def share_view(request, token):
    request.session['share_token'] = token
    return redirect('home')
