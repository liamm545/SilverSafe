# Silver_Safe

## Purpose
YOLOv8 객체 탐지를 웹 애플리케이션과 Firebase에 통합, 노약자분들의 Pose estimation
- 비디오 스트림에서 pose estimate
- 탐지된 활동에 따라 Firebase 실시간 데이터베이스 업데이트

## Features
- 실시간 객체 탐지: YOLOv8을 사용하여 비디오 스트림에서 실시간으로 객체 및 활동을 탐지
- Firebase 통합: 탐지된 활동을 기반으로 Firebase 실시간 데이터베이스를 업데이트
- 활동 모니터링: 낙상, 점프, 앉기, 서기, 걷기 등의 특정 활동을 탐지

## Prerequisites
- Python 3.8 이상
- OpenCV
- Firebase Admin SDK
- Ultralytics YOLOv8

## Run
프로젝트를 실행하는 방법:

1. local 기반 실행
    ```bash
    python local.py
    ```

2. online 기반 실행
    ```bash
    python online.py
    ```

## Demo
