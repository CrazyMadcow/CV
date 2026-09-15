# 아주대학교 교수 지원용 PDF

공개용 웹페이지(`index.html`)와 분리된 A4 고정 레이아웃 문서입니다.

## 미리보기

VS Code Live Server로 `application/ajou.html`을 엽니다. 화면에서도 A4 6페이지 단위로 표시됩니다.

## PDF 생성

프로젝트 루트의 PowerShell에서 실행합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\application\generate-pdf.ps1
```

생성 파일:

```text
dist/Kwangwoo_Jang_Ajou.pdf
```

실제 프로필 사진과 연구 그림이 준비되면 `../assets/img/`의 현재 이미지를 교체하거나 `ajou.html`에서 파일 경로를 변경합니다.
