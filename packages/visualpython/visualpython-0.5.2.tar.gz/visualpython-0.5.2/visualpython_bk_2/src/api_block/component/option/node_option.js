define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpTableLayoutVerticalSimple'

    , '../../api.js'    

    , '../../constData.js'
    , '../../blockRenderer.js'
    , '../base/index.js'

], function ( $, vpCommon, vpConst, sb, vpTableLayoutVerticalSimple, 
              api,constData, 
              blockRenderer, baseComponent ) {
                  
    const { BLOCK_DIRECTION
            , BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , STR_NULL
            , STR_ONE_INDENT
        
            , NUM_MAX_ITERATION
        
            , ERROR_AB0002_INFINITE_LOOP } = constData;

    const { MakeOptionContainer
            , MakeOptionDeleteButton
            , MakeOptionPlusButton
            , MakeVpSuggestInputText_apiblock
            , MakeOptionInput
            , MakeOptionSelectBox } = baseComponent;
    // var code = STR_MSG_AUTO_GENERATED_BY_VISUALPYTHON + ' - ' +'API Block' + STR_KEYWORD_NEW_LINE;
    var InitNodeBlockOption = function(thatBlock, optionPageSelector) {
        var blockContainerThis = thatBlock.getBlockContainerThis();

        /** List For option 렌더링 */
        var renderThisComponent = function() {
            var nodeBlockOption = MakeOptionContainer();

            var childLowerDepthBlockList = thatBlock.getChildLowerDepthBlockList();
            var rootDepth = thatBlock.getDepth();
            childLowerDepthBlockList.forEach( ( block ) => {
                if ( block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER ) {
                    return;
                }
                var depth = block.getDepth() - rootDepth;
              
                var indentPxStr = STR_NULL;
                var iteration = 0;
                while ( depth-- != 0) {
                    indentPxStr += STR_ONE_INDENT;
                    if (iteration > NUM_MAX_ITERATION) {
                        console.log(ERROR_AB0002_INFINITE_LOOP);
                        break;
                    }
                    iteration++;
                }
                
                var code = indentPxStr + block.setCodeLineAndGet();
                var codeDom = $(`<div style="white-space: break-spaces; 
                                            font-size: 16px;
                                            margin-top:2.5px;">${code}</div>`);
                nodeBlockOption.append(codeDom);
            });

            $(optionPageSelector).append(nodeBlockOption);
        }
        renderThisComponent();
    }       
    return InitNodeBlockOption;
});