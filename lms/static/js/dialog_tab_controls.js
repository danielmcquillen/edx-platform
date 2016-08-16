var DialogTabControls = (function() {
    'use strict';

    var focusableChildren,
        numElements,
        currentIndex,
        setCurrentIndex = function(currentElement) {
            var elementIndex = focusableChildren.index(currentElement);
            if (elementIndex >= 0) {
                currentIndex = elementIndex;
            }
        },
        initializeTabKeyValues = function(elementName, $closeButton) {
            focusableChildren = $(elementName).find(
                'a, input[type=text], input[type=submit], select, textarea, button'
            );
            if ($closeButton) {
                focusableChildren = focusableChildren.add($closeButton);
            }
            numElements = focusableChildren.length;
            currentIndex = 0;
            focusableChildren[currentIndex].focus();
            focusableChildren.on('click', function() {
                setCurrentIndex(this);
            });
        },
        focusElement = function() {
            var focusableElement = focusableChildren[currentIndex];
            if (focusableElement) {
                focusableElement.focus();
            }
        },
        focusPrevious = function() {
            currentIndex--;
            if (currentIndex < 0) {
                currentIndex = numElements - 1;
            }

            focusElement();

            return false;
        },
        focusNext = function() {
            currentIndex++;
            if (currentIndex >= numElements) {
                currentIndex = 0;
            }

            focusElement();

            return false;
        },
        setKeydownListener = function($modal, $closeButton) {
            $modal.on('keydown', function(e) {
                var keyCode = e.keyCode || e.which,
                    escapeKeyCode = 27,
                    tabKeyCode = 9;
                if (keyCode === escapeKeyCode) {
                    e.preventDefault();
                    $closeButton.click();
                }
                if (keyCode === tabKeyCode && e.shiftKey) {
                    e.preventDefault();
                    focusPrevious();
                } else if (keyCode === tabKeyCode) {
                    e.preventDefault();
                    focusNext();
                }
            });
        };

    return {
        initializeTabKeyValues: initializeTabKeyValues,
        setKeydownListener: setKeydownListener
    };
}());
