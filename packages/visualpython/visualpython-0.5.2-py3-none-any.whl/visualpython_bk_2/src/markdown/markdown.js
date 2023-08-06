define([
    'require'
    , 'jquery'
    , 'notebook/js/mathjaxutils'
    , 'components/marked/lib/marked'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/common/component/vpLineNumberTextArea'
], function (requirejs, $, mathjaxutils, marked, vpCommon, vpConst, sb, vpFuncJS, vpLineNumberTextArea) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "Markdown"
        , funcID : "com_markdown"
    }

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     * @param {JSON} meta 메타 데이터
     */
    var optionLoadCallback = function(callback, meta) {
        // 컨테이너에서 전달된 callback 함수가 존재하면 실행.
        if (typeof(callback) === 'function') {
            var uuid = vpCommon.getUUID();
            // 최대 10회 중복되지 않도록 체크
            for (var idx = 0; idx < 10; idx++) {
                // 이미 사용중인 uuid 인 경우 다시 생성
                if ($(vpConst.VP_CONTAINER_ID).find("." + uuid).length > 0) {
                    uuid = vpCommon.getUUID();
                }
            }
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM))).find(vpCommon.formatString(".{0}", vpConst.API_OPTION_PAGE)).addClass(uuid);
            // 옵션 객체 생성
            var mMarkdown = new Markdown(uuid);
            mMarkdown.metadata = meta;
            
            // 옵션 속성 할당.
            mMarkdown.setOptionProp(funcOptProp);
            // html 설정.
            mMarkdown.initHtml();
            callback(mMarkdown);  // 공통 객체를 callback 인자로 전달
        }
    }
    
    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     * @param {JSON} meta 메타 데이터
     */
    var initOption = function(callback, meta) {
        vpCommon.loadHtml(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM)), "markdown/markdown.html", optionLoadCallback, callback, meta);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var Markdown = function(uuid) {
        this.uuid = uuid;   // Load html 영역의 uuid.
        this.packageList = [
            {}
        ]
        this.package = {
            id: 'com_markdown',
            name: 'Markdown',
            library: 'common',
            description: '마크다운',
            input: [
                {
                    name: vpCommon.formatString("{0}{1}", vpConst.VP_ID_PREFIX, "markdownEditor")
                }
            ]
        }
    }

    /**
     * vpFuncJS 에서 상속
     */
    Markdown.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
     */
    Markdown.prototype.optionValidation = function() {
        return true;

        // 부모 클래스 유효성 검사 호출.
        // vpFuncJS.VpFuncJS.prototype.optionValidation.apply(this);
    }

    /**
     * html 내부 binding 처리
     */
    Markdown.prototype.initHtml = function() {
        var sbPageContent = new sb.StringBuilder();

        var lineNumberTextArea = new vpLineNumberTextArea.vpLineNumberTextArea(vpCommon.formatString("{0}{1}", vpConst.VP_ID_PREFIX, "markdownEditor"));
        sbPageContent.appendLine(lineNumberTextArea.toTagString());
        sbPageContent.appendFormatLine("<div class='rendered_html' id='{0}{1}'></div>", vpConst.VP_ID_PREFIX, "markdownPreview");

        this.setPage(sbPageContent.toString());

        // 상단 에디터 메뉴 추가
        addEditorOptionLine($(this.wrapSelector(vpCommon.formatString(".{0}", lineNumberTextArea._UUID))));

        $(this.wrapSelector(vpCommon.formatString(".{0}", lineNumberTextArea._UUID))).css({
            width: "calc(100% - 20px)"
            , margin: "10px"
        });
        $(this.wrapSelector("textarea")).css("height", "165px");
        $(this.wrapSelector(vpCommon.formatString("#{0}{1}", vpConst.VP_ID_PREFIX, "markdownPreview"))).css({
            width: "calc(100% - 20px)"
            , margin: "20px 10px 5px 10px"
            , "max-height": "300px"
            , overflow: "auto"
        })
    }

    // 상단 에디터 메뉴 추가
    var addEditorOptionLine = function(target) {
        var sbEditorOptionLine = new sb.StringBuilder();

        sbEditorOptionLine.appendFormatLine("<div class='{0}'>", vpConst.VP_MARKDOWN_EDITOR_TOOLBAR);

        sbEditorOptionLine.appendFormatLine("<div class='{0}'></div>", vpConst.VP_MARKDOWN_TOOBAR_BTN_TITLE);
        sbEditorOptionLine.appendFormatLine("<div class='{0}'></div>", vpConst.VP_MARKDOWN_TOOBAR_BTN_BOLD);
        sbEditorOptionLine.appendFormatLine("<div class='{0}'></div>", vpConst.VP_MARKDOWN_TOOBAR_BTN_ITALIC);
        sbEditorOptionLine.appendFormatLine("<div class='{0}'></div>", vpConst.VP_MARKDOWN_TOOBAR_BTN_CODE);
        // sbEditorOptionLine.appendFormatLine("<div class='{0}'></div>", vpConst.VP_MARKDOWN_TOOBAR_BTN_LINK);
        sbEditorOptionLine.appendFormatLine("<div class='{0}'></div><input type='file' class='{1}'/>"
            , vpConst.VP_MARKDOWN_TOOBAR_BTN_IMAGE, vpConst.VP_MARKDOWN_TOOBAR_INPUT_FILE_IMAGE);

        sbEditorOptionLine.appendLine("</div>");
        
        $(sbEditorOptionLine.toString()).prependTo(target);
    }

    /**
     * 코드 생성
     * @param {boolean} addCell 셀에 추가
     * @param {boolean} exec 실행여부
     */
    Markdown.prototype.generateCode = function(addCell = false, exec = false) {
        this.generatedCode = $(this.wrapSelector(vpCommon.formatString("#{0}{1}", vpConst.VP_ID_PREFIX, "markdownEditor"))).val();
        if (addCell) {
            this.cellExecute(this.generatedCode, exec, "markdown");
        }

        return this.generatedCode;
    }

    /**
     * 옵션내 이벤트 바인딩.
     */
    Markdown.prototype.bindOptionEvent = function() {
        var that = this;
        $(document).on(vpCommon.formatString("propertychange change keyup paste input.{0}", that.uuid), that.wrapSelector(vpCommon.formatString("#{0}{1}", vpConst.VP_ID_PREFIX, "markdownEditor")), function(evt) {
            previewRender($(this).val());
        });

        $(document).on(vpCommon.formatString("click.{0}", that.uuid), that.wrapSelector(vpCommon.formatString(".{0} div[class^={1}]", vpConst.VP_MARKDOWN_EDITOR_TOOLBAR, vpConst.VP_MARKDOWN_TOOBAR_BTN)), function(evt) {
            // jquery object convert to javascript object for get selection properies
            var textarea = $(vpCommon.formatString(".{0} #{1}{2}", that.uuid, vpConst.VP_ID_PREFIX, "markdownEditor")).get(0);
            if ($(this).hasClass(vpConst.VP_MARKDOWN_TOOBAR_BTN_TITLE)) {
                adjustTitle(textarea);
            } else if ($(this).hasClass(vpConst.VP_MARKDOWN_TOOBAR_BTN_BOLD)) {
                adjustBold(textarea);
            } else if ($(this).hasClass(vpConst.VP_MARKDOWN_TOOBAR_BTN_ITALIC)) {
                adjustItalic(textarea);
            } else if ($(this).hasClass(vpConst.VP_MARKDOWN_TOOBAR_BTN_CODE)) {
                adjustCode(textarea);
            } else if ($(this).hasClass(vpConst.VP_MARKDOWN_TOOBAR_BTN_LINK)) {
                console.log("link");
            } else if ($(this).hasClass(vpConst.VP_MARKDOWN_TOOBAR_BTN_IMAGE)) {
                // 클릭시 hidden file control 오픈처리. 선택시 처리는 hidden file control onChange에서 처리
                $(this).parent().children(vpCommon.formatString(".{0}", vpConst.VP_MARKDOWN_TOOBAR_INPUT_FILE_IMAGE)).click();
            }
            
            // 이미지 로드의 경우 처리단계에서 랜더링 호출 하므로 이곳에서 호출하면 중복
            if (!$(this).hasClass(vpConst.VP_MARKDOWN_TOOBAR_BTN_IMAGE)) {
                // 마크다운 렌더링 시행
                previewRender(textarea.value);
            }
        });
        
        $(document).on(vpCommon.formatString("change.{0}", that.uuid), that.wrapSelector(vpCommon.formatString(".{0}", vpConst.VP_MARKDOWN_TOOBAR_INPUT_FILE_IMAGE)), function(evt) {
            // jquery object convert to javascript object for get selection properies
            var textarea = $(vpCommon.formatString(".{0} #{1}{2}", that.uuid, vpConst.VP_ID_PREFIX, "markdownEditor")).get(0);

            importImage(textarea, evt.target.files[0]);
        });
    }

    /**
     * 마크다운 렌더링
     * @param {String} text 렌더링할 텍스트
     */
    var previewRender = function(text) {
        var math = null;
        var text_and_math = mathjaxutils.remove_math(text);
        text = text_and_math[0];
        math = text_and_math[1];

        var renderer = new marked.Renderer();

        marked(text, { renderer: renderer }, function (err, html) {
            html = mathjaxutils.replace_math(html, math);
            document.getElementById(vpCommon.formatString("{0}{1}", vpConst.VP_ID_PREFIX, "markdownPreview")).innerHTML = html;

            MathJax.Hub.Queue(["Typeset", MathJax.Hub, vpCommon.formatString("{0}{1}", vpConst.VP_ID_PREFIX, "markdownPreview")]);
        });
    }

    /**
     * 타이틀 설정
     * @param {object} textarea 마크다운 에디터 입력창
     */
    var adjustTitle = function(textarea) {
        // 커서 위치
        var cursorPosition = 0;
        // 선택영역 시작과 끝이 같으면 선택 영역이 없는 현재 커서 위치
        if (textarea.selectionStart == textarea.selectionEnd) {
            cursorPosition = textarea.selectionStart;
        } else { // 선택영역 시작과 끝이 다르면 선택 방향에 따라서 잡아준다.
            cursorPosition = textarea.selectionDirection == "forward" ? textarea.selectionEnd : textarea.selectionStart;
        }

        // 커서 기준 앞 전체 텍스트
        var preText = textarea.value.substring(0, cursorPosition);
        // 커서 기준 뒤 전체 텍스트
        var postText = textarea.value.substring(cursorPosition);
        // 커서 기준 현재 라인
        var lineText = preText.substring(preText.lastIndexOf('\n') + 1) + postText.substring(0, postText.indexOf('\n'));
        // 빈 라인이면 default text로 변경해준다.
        if (lineText.trim() == "") {
            lineText = vpConst.VP_MARKDOWN_DEFAULT_NEW_TITLE_TEXT;
        }
        var adjustText;
        // 현재 라인이 타이틀 마크다운으로 되어 있는지 확인
        if (/^[#]{6}\s{1,}/i.test(lineText)) { // #이 6개면 1개로 되돌린다.
            adjustText = preText.substring(0, preText.lastIndexOf('\n') + 1) + "#" + lineText.replace("######", "") + postText.substring(postText.indexOf('\n'));
        } else if (/^[#]{1,5}\s{1,}/i.test(lineText)) { // #이 1개에서 5개사이면 #한개 추가한다
            adjustText = preText.substring(0, preText.lastIndexOf('\n') + 1) + "#" + lineText + postText.substring(postText.indexOf('\n'));
        } else { // #이 6개를 초과했거나 없으면 #과 1공백문자를 추가한다. 
            adjustText = preText.substring(0, preText.lastIndexOf('\n') + 1) + "# " + lineText + postText.substring(postText.indexOf('\n'));
        }

        // 변경 텍스트 반영
        textarea.value = adjustText;
    }

    /**
     * 볼드체 설정
     * @param {object} textarea 마크다운 에디터 입력창
     */
    var adjustBold = function(textarea) {
        // 정규식
        let regExp = /^[*]{2}(.*?)[*]{2}$/;
        // 선택된 텍스트
        var selectedText = textarea.value.substring(textarea.selectionStart, textarea.selectionEnd);
        
        var targetText = "";    // 비교대상 텍스트
        var adjustText;         // 변형 결과 텍스트
        var preCheck = true;    // 기준 앞 비교 필요 여부
        var postCheck = true;   // 기준 뒤 비교 필요 여부
        var nIdx = 0;           // 반복문에서 사용할 카운터
        var preShiftCount = 0;  // 대상 앞 시프트 카운트
        var postShiftCount = 0; // 대상 뒤 시프트 카운트

        // 커서 기준 앞 전체 텍스트
        var preText = textarea.value.substring(0, textarea.selectionStart);
        // 커서 기준 뒤 전체 텍스트
        var postText = textarea.value.substring(textarea.selectionEnd);

        // 선택 영역이 없는경우 디폴트 텍스트로 볼드 입력
        if (textarea.selectionStart == textarea.selectionEnd) {
            var checkChar;
            var preCheckChar;
            // 커서 앞으로 체크
            while (true) {
                nIdx++;
                preCheckChar = checkChar;
                checkChar = textarea.value.charAt(textarea.selectionStart - nIdx);
                // *가 끝나면 중지
                if (preCheckChar == "*" && checkChar != "*") break;
                // 문자가 없거나 공백이거나 개행이면 중지
                if (checkChar == "" || checkChar == " " || checkChar == '\n') {
                    break;
                } else {
                    targetText = checkChar + targetText;
                    preShiftCount++;
                }
            }
            // 커서 뒤로 체크
            nIdx = 0;
            while (true) {
                preCheckChar = checkChar;
                checkChar = textarea.value.charAt(textarea.selectionStart + nIdx);
                // *가 끝나면 중지
                if (preCheckChar == "*" && checkChar != "*") break;
                // 문자가 없거나 공백이거나 개행이면 중지
                if (checkChar == "" || checkChar == " " || checkChar == '\n') {
                    break;
                } else {
                    targetText = targetText + checkChar;
                    postShiftCount++;
                }
                nIdx++;
            }

            // targetText로 포함시킨 만큼 preText, postText 잘라내기
            // 잘라낸게 존재하면 slice
            if (preShiftCount != 0) {
                preText = preText.slice(0, -preShiftCount);
            }
            postText = postText.substring(postShiftCount);

            // 볼드체를 제거할지 추가할지 판단
            if (regExp.test(targetText.trim())) { // ** ** 로 감싸져 있어 볼드 제거
                adjustText = preText + targetText.slice(2, -2) + postText;
            } else {
                // 대상 텍스트가 없거나 *를 포함하는 경우는 커서 단어(공백) 뒤에 디폴트 텍스트 추가
                if (targetText == "" || targetText.indexOf("*") > -1) {
                    adjustText = preText + targetText + (targetText == "" ? "**" : " **") + vpConst.VP_MARKDOWN_DEFAULT_BOLD_TEXT + "**" + postText;
                } else { // 대상 텍스트에 대하여 볼드체 추가
                    adjustText = preText + "**" + targetText + "**" + postText;
                }
            }
        } else { // 선택영역이 있는경우 볼드체를 제거할지 추가할지 판단
            targetText = selectedText;
    
            // selectedText 앞뒤로 * 가 아닌것 만날때까지 targetText에 추가.
            for (nIdx = 0; nIdx < 3; nIdx++) {
                // 선택영역 앞으로 * 가 붙어있는경우 확장해준다.
                if (preCheck && textarea.value.charAt(textarea.selectionStart - (nIdx + 1)) === "*") {
                    targetText = "*" + targetText;
                    preShiftCount++;
                } else { // 선택영역 앞이 * 가 아닌경우 범위 확장 중지
                    preCheck = false;
                }
                // 선택영역 뒤로 * 가 붙어있는경우 확장해준다.
                if (postCheck && textarea.value.charAt(textarea.selectionEnd + nIdx) === "*") {
                    targetText = targetText + "*";
                    postShiftCount++;
                } else { // 선택영역 뒤가 * 가 아닌경우 범위 확장 중지
                    postCheck = false;
                }
            }
            
            // 볼드체를 제거할지 추가할지 판단
            if (regExp.test(targetText.trim())) { // ** ** 로 감싸져 있어 볼드 제거
                // targetText로 포함시킨 만큼 preText, postText 잘라내기
                // 잘라낸게 존재하면 slice
                if (preShiftCount != 0) {
                    preText = preText.slice(0, -preShiftCount);
                }
                postText = postText.substring(postShiftCount);

                adjustText = preText + targetText.slice(2, -2) + postText;
            } else {
                adjustText = preText + "**" + targetText + "**" + postText;
            }
        }

        // 변경 텍스트 반영
        textarea.value = adjustText;
    }

    /**
     * 이탈릭체 설정
     * @param {object} textarea 마크다운 에디터 입력창
     */
    var adjustItalic = function(textarea) {
        // 정규식
        let regExp = /^[*]{1}(.*?)[*]{1}$/;
        // 선택된 텍스트
        var selectedText = textarea.value.substring(textarea.selectionStart, textarea.selectionEnd);
        
        var targetText = "";    // 비교대상 텍스트
        var adjustText;         // 변형 결과 텍스트
        var preCheck = true;    // 기준 앞 비교 필요 여부
        var postCheck = true;   // 기준 뒤 비교 필요 여부
        var nIdx = 0;           // 반복문에서 사용할 카운터
        var preShiftCount = 0;  // 대상 앞 시프트 카운트
        var postShiftCount = 0; // 대상 뒤 시프트 카운트

        // 커서 기준 앞 전체 텍스트
        var preText = textarea.value.substring(0, textarea.selectionStart);
        // 커서 기준 뒤 전체 텍스트
        var postText = textarea.value.substring(textarea.selectionEnd);

        // 선택 영역이 없는경우 디폴트 텍스트로 이탈릭 입력
        if (textarea.selectionStart == textarea.selectionEnd) {
            var checkChar;
            var preCheckChar;
            // 커서 앞으로 체크
            while (true) {
                nIdx++;
                preCheckChar = checkChar;
                checkChar = textarea.value.charAt(textarea.selectionStart - nIdx);
                if (preCheckChar == "*" && checkChar != "*") break;
                // 문자가 없거나 공백이거나 개행이면 중지
                if (checkChar == "" || checkChar == " " || checkChar == '\n') {
                    break;
                } else {
                    targetText = checkChar + targetText;
                    preShiftCount++;
                }
            }
            // 커서 뒤로 체크
            nIdx = 0;
            while (true) {
                preCheckChar = checkChar;
                checkChar = textarea.value.charAt(textarea.selectionStart + nIdx);
                if (preCheckChar == "*" && checkChar != "*") break;
                // 문자가 없거나 공백이거나 개행이면 중지
                if (checkChar == "" || checkChar == " " || checkChar == '\n') {
                    break;
                } else {
                    targetText = targetText + checkChar;
                    postShiftCount++;
                }
                nIdx++;
            }

            // targetText로 포함시킨 만큼 preText, postText 잘라내기
            // 잘라낸게 존재하면 slice
            if (preShiftCount != 0) {
                preText = preText.slice(0, -preShiftCount);
            }
            postText = postText.substring(postShiftCount);

            // 이탈릭체를 제거할지 추가할지 판단
            if (regExp.test(targetText.trim())) { // * * 로 감싸져 있어 이탈릭 제거
                adjustText = preText + targetText.slice(1, -1) + postText;
            } else {
                // 대상 텍스트가 없거나 *를 포함하는 경우는 커서 단어(공백) 뒤에 디폴트 텍스트 추가
                if (targetText == "" || targetText.indexOf("*") > -1) {
                    adjustText = preText + targetText + (targetText == "" ? "*" : " *") + vpConst.VP_MARKDOWN_DEFAULT_ITALIC_TEXT + "*" + postText;
                } else { // 대상 텍스트에 대하여 이탈릭체 추가
                    adjustText = preText + "*" + targetText + "*" + postText;
                }
            }
        } else { // 선택영역이 있는경우 이탈릭체를 제거할지 추가할지 판단
            targetText = selectedText;
    
            // selectedText 앞뒤로 * 가 아닌것 만날때까지 targetText에 추가.
            for (nIdx = 0; nIdx < 3; nIdx++) {
                // 선택영역 앞으로 * 가 붙어있는경우 확장해준다.
                if (preCheck && textarea.value.charAt(textarea.selectionStart - (nIdx + 1)) === "*") {
                    targetText = "*" + targetText;
                    preShiftCount++;
                } else { // 선택영역 앞이 * 가 아닌경우 범위 확장 중지
                    preCheck = false;
                }
                // 선택영역 뒤로 * 가 붙어있는경우 확장해준다.
                if (postCheck && textarea.value.charAt(textarea.selectionEnd + nIdx) === "*") {
                    targetText = targetText + "*";
                    postShiftCount++;
                } else { // 선택영역 뒤가 * 가 아닌경우 범위 확장 중지
                    postCheck = false;
                }
            }
            
            // 이탈릭체를 제거할지 추가할지 판단
            if (regExp.test(targetText.trim())) { // * * 로 감싸져 있어 이탈릭 제거
                // targetText로 포함시킨 만큼 preText, postText 잘라내기
                // 잘라낸게 존재하면 slice
                if (preShiftCount != 0) {
                    preText = preText.slice(0, -preShiftCount);
                }
                postText = postText.substring(postShiftCount);

                adjustText = preText + targetText.slice(1, -1) + postText;
            } else {
                adjustText = preText + "*" + targetText + "*" + postText;
            }
        }

        // 변경 텍스트 반영
        textarea.value = adjustText;
    }

    /**
     * 코드체 설정
     * @param {object} textarea 마크다운 에디터 입력창
     */
    var adjustCode = function(textarea) {
        // 정규식
        let regExp = /^[`]{1}(.*?)[`]{1}$/;
        // 선택된 텍스트
        var selectedText = textarea.value.substring(textarea.selectionStart, textarea.selectionEnd);
        
        var targetText = "";    // 비교대상 텍스트
        var adjustText;         // 변형 결과 텍스트
        var preCheck = true;    // 기준 앞 비교 필요 여부
        var postCheck = true;   // 기준 뒤 비교 필요 여부
        var nIdx = 0;           // 반복문에서 사용할 카운터
        var preShiftCount = 0;  // 대상 앞 시프트 카운트
        var postShiftCount = 0; // 대상 뒤 시프트 카운트

        // 커서 기준 앞 전체 텍스트
        var preText = textarea.value.substring(0, textarea.selectionStart);
        // 커서 기준 뒤 전체 텍스트
        var postText = textarea.value.substring(textarea.selectionEnd);

        // 선택 영역이 없는경우 디폴트 텍스트로 코드 입력
        if (textarea.selectionStart == textarea.selectionEnd) {
            var checkChar;
            var preCheckChar;
            // 커서 앞으로 체크
            while (true) {
                nIdx++;
                preCheckChar = checkChar;
                checkChar = textarea.value.charAt(textarea.selectionStart - nIdx);
                if (preCheckChar == "`" && checkChar != "`") break;
                // 문자가 없거나 공백이거나 개행이면 중지
                if (checkChar == "" || checkChar == " " || checkChar == '\n') {
                    break;
                } else {
                    targetText = checkChar + targetText;
                    preShiftCount++;
                }
            }
            // 커서 뒤로 체크
            nIdx = 0;
            while (true) {
                preCheckChar = checkChar;
                checkChar = textarea.value.charAt(textarea.selectionStart + nIdx);
                if (preCheckChar == "`" && checkChar != "`") break;
                // 문자가 없거나 공백이거나 개행이면 중지
                if (checkChar == "" || checkChar == " " || checkChar == '\n') {
                    break;
                } else {
                    targetText = targetText + checkChar;
                    postShiftCount++;
                }
                nIdx++;
            }

            // targetText로 포함시킨 만큼 preText, postText 잘라내기
            // 잘라낸게 존재하면 slice
            if (preShiftCount != 0) {
                preText = preText.slice(0, -preShiftCount);
            }
            postText = postText.substring(postShiftCount);

            // 코드체를 제거할지 추가할지 판단
            if (regExp.test(targetText.trim())) { // ` ` 로 감싸져 있어 코드 제거
                adjustText = preText + targetText.slice(1, -1) + postText;
            } else {
                // 대상 텍스트가 없거나 `를 포함하는 경우는 커서 단어(공백) 뒤에 디폴트 텍스트 추가
                if (targetText == "" || targetText.indexOf("`") > -1) {
                    adjustText = preText + targetText + "\n\n```\n# " + vpConst.VP_MARKDOWN_DEFAULT_CODE_TEXT + "\n```\n\n\n" + postText;
                } else { // 대상 텍스트에 대하여 코드체 추가
                    adjustText = preText + "`" + targetText + "`" + postText;
                }
            }
        } else { // 선택영역이 있는경우 코드체를 제거할지 추가할지 판단
            targetText = selectedText;
    
            // selectedText 앞뒤로 ` 가 아닌것 만날때까지 targetText에 추가.
            for (nIdx = 0; nIdx < 3; nIdx++) {
                // 선택영역 앞으로 ` 가 붙어있는경우 확장해준다.
                if (preCheck && textarea.value.charAt(textarea.selectionStart - (nIdx + 1)) === "`") {
                    targetText = "`" + targetText;
                    preShiftCount++;
                } else { // 선택영역 앞이 ` 가 아닌경우 범위 확장 중지
                    preCheck = false;
                }
                // 선택영역 뒤로 ` 가 붙어있는경우 확장해준다.
                if (postCheck && textarea.value.charAt(textarea.selectionEnd + nIdx) === "`") {
                    targetText = targetText + "`";
                    postShiftCount++;
                } else { // 선택영역 뒤가 ` 가 아닌경우 범위 확장 중지
                    postCheck = false;
                }
            }
            
            // 코드체를 제거할지 추가할지 판단
            if (regExp.test(targetText.trim())) { // ` ` 로 감싸져 있어 코드 제거
                // targetText로 포함시킨 만큼 preText, postText 잘라내기
                // 잘라낸게 존재하면 slice
                if (preShiftCount != 0) {
                    preText = preText.slice(0, -preShiftCount);
                }
                postText = postText.substring(postShiftCount);

                adjustText = preText + targetText.slice(1, -1) + postText;
            } else {
                adjustText = preText + "`" + targetText + "`" + postText;
            }
        }

        // 변경 텍스트 반영
        textarea.value = adjustText;
    }

    /**
     * 선택된 이미지 파일 인코딩하여 첨부
     * @param {object} textarea 마크다운 에디터 입력창
     * @param {object} file 선택된 파일 정보
     */
    var importImage = function(textarea, file) {
        // 커서 위치
        var cursorPosition = 0;
        // 선택영역 시작과 끝이 같으면 선택 영역이 없는 현재 커서 위치
        if (textarea.selectionStart == textarea.selectionEnd) {
            cursorPosition = textarea.selectionStart;
        } else { // 선택영역 시작과 끝이 다르면 선택 방향에 따라서 잡아준다.
            cursorPosition = textarea.selectionDirection == "forward" ? textarea.selectionEnd : textarea.selectionStart;
        }

        // 커서 기준 앞 전체 텍스트
        var preText = textarea.value.substring(0, cursorPosition);
        // 커서 기준 뒤 전체 텍스트
        var postText = textarea.value.substring(cursorPosition);

        var fileReader = new FileReader();
        fileReader.onload = function() {
            textarea.value = vpCommon.formatString("{0}![{1}]({2}){3}", preText, file.name, fileReader.result, postText);
            previewRender(textarea.value);
        }
        fileReader.readAsDataURL(file);
    }

    /**
     * 메타데이터 로드 후 액션
     * @param {funcJS} option
     * @param {JSON} meta 
     */   
    Markdown.prototype.loadMetaExpend = function(funcJS, meta) {
        previewRender($(vpCommon.formatString("#{0}{1}", vpConst.VP_ID_PREFIX, "markdownEditor")).val());
    }

    return {
        initOption: initOption
    };
});
