from django.shortcuts import render, redirect, get_object_or_404
from .models import DetectionTool, BusinessDetectionTool, PreDetectionRequest
from .forms import BusinessDetectionToolForm, PreDetectionRequestForm
from django.http import FileResponse

def project_list(request):
    return render(request, 'detection/home.html')



# 检测工具管理
def detection_tools_list(request):
    tools = BusinessDetectionTool.objects.filter(user=request.user)
    return render(request, 'detection_tools_list.html', {'tools': tools})

def detection_tools_add(request):
    if request.method == 'POST':
        form = BusinessDetectionToolForm(request.POST)
        if form.is_valid():
            for tool in form.cleaned_data['tools']:
                BusinessDetectionTool.objects.get_or_create(user=request.user, tool=tool)
            return redirect('detection_tools_list')
    else:
        form = BusinessDetectionToolForm()
    return render(request, 'detection_tools_add.html', {'form': form})

# 预检测管理
def pre_detection_list(request):
    detections = PreDetectionRequest.objects.filter(user=request.user)
    return render(request, 'pre_detection_list.html', {'detections': detections})

def pre_detection_add(request):
    if request.method == 'POST':
        form = PreDetectionRequestForm(request.POST)
        if form.is_valid():
            detection = form.save(commit=False)
            detection.user = request.user
            detection.save()
            form.save_m2m()
            # TODO: 调用 SDK 执行检测，并更新状态和报告
            return redirect('pre_detection_list')
    else:
        form = PreDetectionRequestForm()
    return render(request, 'pre_detection_add.html', {'form': form})

def pre_detection_download(request, pk):
    detection = get_object_or_404(PreDetectionRequest, pk=pk, user=request.user)
    if detection.report_file:
        return FileResponse(detection.report_file.open('rb'), as_attachment=True, filename=detection.report_file.name)
    return redirect('pre_detection_list')


