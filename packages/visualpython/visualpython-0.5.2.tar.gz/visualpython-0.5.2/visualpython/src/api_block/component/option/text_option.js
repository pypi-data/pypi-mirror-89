define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpSuggestInputText'
    , '../../api.js'    
 
    , '../../constData.js'
    , '../../blockRenderer.js'
    , '../base/index.js'
], function ( $, vpCommon, vpConst, sb, vpSuggestInputText, api, constData, blockRenderer, baseComponent ) {
    const { ChangeOldToNewState
        , FindStateValue

        , CreateOneArrayValueAndGet
        , UpdateOneArrayValueAndGet
        , DeleteOneArrayValueAndGet

        , DestructureFromBlockArray

        , MakeFirstCharToUpperCase
        , MapTypeToName
        , RemoveSomeBlockAndGetBlockList
        , ShuffleArray
        , GetImageUrl
        , ControlToggleInput } = api;

    const {  RenderInputRequiredColor
            , GenerateReturnOutParamList} = blockRenderer;

    const { BLOCK_DIRECTION
            , BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , STR_COLON_SELECTED
            , STR_NULL
            , STR_FOR
            , STR_INPUT
            , STR_CLICK 
            , STR_CHANGE_KEYUP_PASTE
            
            , VP_ID_PREFIX
            , VP_CLASS_APIBLOCK_PARAM_PLUS_BTN
            , VP_CLASS_APIBLOCK_PARAM_DELETE_BTN
            , VP_CLASS_STYLE_WIDTH_95PERCENT
            , VP_CLASS_STYLE_WIDTH_100PERCENT
            , VP_ID_APIBLOCK_OPTION_CODE_ARG
            , STATE_returnOutParamList
            , STATE_customCodeLine } = constData;

    const { MakeOptionContainer
            , MakeOptionDeleteButton
            , MakeOptionPlusButton
            , MakeLineNumberTextArea_apiblock } = baseComponent;

    var InitTextBlockOption = function(thatBlock, optionPageSelector) {
        var uuid = thatBlock.getUUID();

        /** Code option 렌더링 */
        var renderThisComponent = function() {
            var codeState = thatBlock.getState(STATE_customCodeLine);
            var textBlockOption = MakeOptionContainer();

            var textBlockOptionMenu = $(`<div class="vp-markdown-editor-toolbar">
                                            <div class="vp-markdown-editor-toolbar-btn-title"></div>
                                            <div class="vp-markdown-editor-toolbar-btn-bold"></div>
                                            <div class="vp-markdown-editor-toolbar-btn-italic"></div>
                                            <div class="vp-markdown-editor-toolbar-btn-code"></div>
                                            <div class="vp-markdown-editor-toolbar-btn-link"></div>
                                        </div>`);
            var lineNumberTextAreaStr = MakeLineNumberTextArea_apiblock(VP_ID_APIBLOCK_OPTION_CODE_ARG + uuid, 
                codeState); 
          
            textBlockOption.append(textBlockOptionMenu);
            textBlockOption.append(lineNumberTextAreaStr);
            /** bottom block option 탭에 렌더링된 dom객체 생성 */
            $(optionPageSelector).append(textBlockOption);
        }

        renderThisComponent();
    }

    return InitTextBlockOption;
});