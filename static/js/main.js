(function ($) {
    "use strict";

    /*****************************
    * Commons Variables
    *****************************/
    var $window = $(window),
    $body = $('body');
    
    /****************************
    * Sticky Menu
    *****************************/
    $(window).on('scroll',function() {    
        var scroll = $(window).scrollTop();
        if (scroll < 100) {
         $(".sticky-header").removeClass("sticky");
        }else{
         $(".sticky-header").addClass("sticky");
        }
    });


    /*****************************
    * Off Canvas Function
    *****************************/
    (function () {
        var $offCanvasToggle = $('.offcanvas-toggle'),
            $offCanvas = $('.offcanvas'),
            $offCanvasOverlay = $('.offcanvas-overlay'),
            $mobileMenuToggle = $('.mobile-menu-toggle');
            $offCanvasToggle.on('click', function (e) {
                e.preventDefault();
                var $this = $(this),
                    $target = $this.attr('href');
                $body.addClass('offcanvas-open');
                $($target).addClass('offcanvas-open');
                $offCanvasOverlay.fadeIn();
                if ($this.parent().hasClass('mobile-menu-toggle')) {
                    $this.addClass('close');
                }
            });
            $('.offcanvas-close, .offcanvas-overlay').on('click', function (e) {
                e.preventDefault();
                $body.removeClass('offcanvas-open');
                $offCanvas.removeClass('offcanvas-open');
                $offCanvasOverlay.fadeOut();
                $mobileMenuToggle.find('a').removeClass('close');
            });
    })();


    /**************************
     * Offcanvas: Menu Content
     **************************/
    function mobileOffCanvasMenu() {
        var $offCanvasNav = $('.offcanvas-menu'),
            $offCanvasNavSubMenu = $offCanvasNav.find('.mobile-sub-menu');

        /*Add Toggle Button With Off Canvas Sub Menu*/
        $offCanvasNavSubMenu.parent().prepend('<div class="offcanvas-menu-expand"></div>');

        /*Category Sub Menu Toggle*/
        $offCanvasNav.on('click', 'li a, .offcanvas-menu-expand', function (e) {
            var $this = $(this);
            if ($this.attr('href') === '#' || $this.hasClass('offcanvas-menu-expand')) {
                e.preventDefault();
                if ($this.siblings('ul:visible').length) {
                    $this.parent('li').removeClass('active');
                    $this.siblings('ul').slideUp();
                    $this.parent('li').find('li').removeClass('active');
                    $this.parent('li').find('ul:visible').slideUp();
                } else {
                    $this.parent('li').addClass('active');
                    $this.closest('li').siblings('li').removeClass('active').find('li').removeClass('active');
                    $this.closest('li').siblings('li').find('ul:visible').slideUp();
                    $this.siblings('ul').slideDown();
                }
            }
        });
    }
    mobileOffCanvasMenu();


    /******************************
     * Hero Slider - [Single Grid]
     *****************************/
    $('.hero-area-wrapper').slick({
        arrows: false,
        fade: true,
        dots: true,
        easing: 'linear',
        speed: 2000,
    });

    /******************************
     * CartIconSlider - 
     *****************************/

     function createHeartIc(el) {
        var el = el,
            span = el.querySelector('span'),
            svg = span.querySelector('svg'),
            opacityCurve = mojs.easing.path('M0,0 C0,87 27,100 40,100 L40,0 L100,0'),
            scaleCurve = mojs.easing.path('M0,0c0,80,39.2,100,39.2,100L40-100c0,0-0.7,106,60,106'),
            burst = new mojs.Burst({
                parent: el,
                duration: 1200,
                delay: 200,
                shape: 'circle',
                fill: '#E87171',
                x: '50%', y: '50%',
                opacity: {1:0},
                childOptions: { 
                    radius: {6:0},
                    type: 'line',
                    stroke: '#E87171',
                    strokeWidth: 2
                },
                radius: {0:32},
                count: 7,
                //isSwirl: true,
                isRunLess: true,
                easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
            }),
            heart = new Animocon(el, {
                tweens : [
                    /* // ring animation
                    new mojs.Transit({
                        parent: el11,
                        duration: 1000,
                        delay: 100,
                        type: 'circle',
                        radius: {0: 95},
                        fill: 'transparent',
                        stroke: '#C0C1C3',
                        strokeWidth: {50:0},
                        opacity: 0.4,
                        x: '50%',     
                        y: '50%',
                        isRunLess: true,
                        easing: mojs.easing.bezier(0, 1, 0.5, 1)
                    }),
                    // ring animation
                    new mojs.Transit({
                        parent: el11,
                        duration: 1800,
                        delay: 300,
                        type: 'circle',
                        radius: {0: 80},
                        fill: 'transparent',
                        stroke: '#C0C1C3',
                        strokeWidth: {40:0},
                        opacity: 0.2,
                        x: '50%',     
                        y: '50%',
                        isRunLess: true,
                        easing: mojs.easing.bezier(0, 1, 0.5, 1)
                    }), */
                    // icon scale animation
                    
                    burst,
                    
                    new mojs.Tween({
                        duration : 800,
                        easing: mojs.easing.ease.out,
                        onUpdate: function(progress) {
                            var opacityProgress = opacityCurve(progress);
                            span.style.opacity = opacityProgress;
    
                            var scaleProgress = scaleCurve(progress);
                            span.style.WebkitTransform = span.style.transform = 'scale3d(' + scaleProgress + ',' + scaleProgress + ',1)';
    
                            var colorProgress = opacityCurve(progress);
                            svg.style.fill = colorProgress >= 1 ? '#E87171' : 'none';
                            svg.style.stroke = colorProgress >= 1 ? '#E87171' : '#a1a8ad';
                        }
                    })	
                ],
                onUnCheck : function() {
                    svg.style.fill = 'none';
                    svg.style.stroke = '#a1a8ad';
                }
            });
    
        return heart;
    }
    
     
    function createCartIc(el) {
        var el = el,
            span = el.querySelector('span'),
            svg = span.querySelector('svg'),
            body = svg.getElementsByTagName("path")[0],
            opacityCurve = mojs.easing.path('M0,0 C0,87 27,100 40,100 L40,0 L100,0'),
            scaleCurve = mojs.easing.path('M0,0c0,80,39.2,100,39.2,100L40-100c0,0-0.7,106,60,106'),
            burst = new mojs.Burst({
                parent: el,
                duration: 1200,
                delay: 200,
                shape: 'circle',
                fill: '#111111',
                x: '50%', y: '50%',
                opacity: {1:0},
                childOptions: { 
                    radius: {6:2},
                    type: 'line',
                    stroke: '#111111',
                    strokeWidth: 2
                },
                radius: {0:36},
                angle: 45,
                count: 4,
                //isSwirl: true,
                isRunLess: true,
                easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
            }),
            heart = new Animocon(el, {
                tweens : [
                    /* // ring animation
                    new mojs.Transit({
                        parent: el11,
                        duration: 1000,
                        delay: 100,
                        type: 'circle',
                        radius: {0: 95},
                        fill: 'transparent',
                        stroke: '#C0C1C3',
                        strokeWidth: {50:0},
                        opacity: 0.4,
                        x: '50%',     
                        y: '50%',
                        isRunLess: true,
                        easing: mojs.easing.bezier(0, 1, 0.5, 1)
                    }),
                    // ring animation
                    new mojs.Transit({
                        parent: el11,
                        duration: 1800,
                        delay: 300,
                        type: 'circle',
                        radius: {0: 80},
                        fill: 'transparent',
                        stroke: '#C0C1C3',
                        strokeWidth: {40:0},
                        opacity: 0.2,
                        x: '50%',     
                        y: '50%',
                        isRunLess: true,
                        easing: mojs.easing.bezier(0, 1, 0.5, 1)
                    }), */
                    // icon scale animation
                    
                    burst,
                    
                    new mojs.Tween({
                        duration : 800,
                        easing: mojs.easing.ease.out,
                        onUpdate: function(progress) {
                            var opacityProgress = opacityCurve(progress);
                            span.style.opacity = opacityProgress;
    
                            var scaleProgress = scaleCurve(progress);
                            span.style.WebkitTransform = span.style.transform = 'scale3d(' + scaleProgress + ',' + scaleProgress + ',1)';
    
                            var colorProgress = opacityCurve(progress);
                            body.style.fill = colorProgress >= 1 ? '#111111' : 'none';
                            svg.style.stroke = colorProgress >= 1 ? '#111111' : '#a1a8ad';
                        }
                    })	
                ],
                onUnCheck : function() {
                    body.style.fill = 'none';
                    svg.style.stroke = '#a1a8ad';
                }
            });
    
        return heart;
    }
    
    
    var hearts = document.getElementsByClassName('pnl-favorites'),
        carts = document.getElementsByClassName('pnl-tocart');
    
    for (var i=0;i<hearts.length;i++) {
        createHeartIc(hearts[i].querySelector('div'));
        createCartIc(carts[i].querySelector('div'));
    }

    /************************************************
     * Product Slider - Style: Default [4 Grid, 1 Row]
     ***********************************************/
    $('.product-default-slider-4grids-1row').slick({
        arrows: true,
        infinite: false,
        slidesToShow: 4,
        slidesToScroll: 1,
        rows: 1,
        easing: 'ease-out',
        speed: 1000,
        prevArrow: '<button type="button" class="default-slider-arrow default-slider-arrow--left prevArrow"><i class="fa fa-angle-left"></button>',
        nextArrow: '<button type="button"  class="default-slider-arrow default-slider-arrow--right nextArrow"><i class="fa fa-angle-right"></button>',
        responsive: [

            {
                breakpoint: 1200,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2,
                }
            },
            {
                breakpoint: 575,
                settings: {
                    slidesToShow: 1,
                }
            },
        ]
    });

    /************************************************
     * Company logo Slider
     ***********************************************/
    $('.company-logo-slider').slick({
        autoplay: true,
        infinite:true,
        arrows: false,
        slidesToShow: 4,
        slidesToScroll: 1,
        easing: 'linear',
        speed: 1000,
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 4
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 2
                }
            }
        ]
    });
    /***********************************
    * Gallery - Horizontal
    ************************************/
   $('.product-large-image-horaizontal').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.product-image-thumb-horizontal'
    });
    $('.product-image-thumb-horizontal').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        focusOnSelect: true,
        arrows: true,
        asNavFor: '.product-large-image-horaizontal',
        prevArrow: '<button type="button" class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-left prevArrow"><i class="fa fa-angle-left"></i></button>',
        nextArrow: '<button type="button"  class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-right nextArrow"><i class="fa fa-angle-right"></i></button>',
        responsive: [
            {
                breakpoint: 1200,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 2
                }
            }
        ]
    });
    /***********************************
    * Gallery - Vertical
    ************************************/
   $('.product-large-image-vertical').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.product-image-thumb-vertical'
    });
    $('.product-image-thumb-vertical').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        focusOnSelect: true,
        arrows: true,
        vertical: true,
        asNavFor: '.product-large-image-vertical',
        prevArrow: '<button type="button" class="gallery-nav gallery-nav-vertical gallery-nav-vertical-up prevArrow"><i class="fa fa-angle-up"></i></button>',
        nextArrow: '<button type="button"  class="gallery-nav gallery-nav-vertical gallery-nav-vertical-down nextArrow"><i class="fa fa-angle-down"></i></button>',
        responsive: [
            {
                breakpoint: 1200,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 3
                }
            }
        ]
    });

    
    /********************************
    *  Product Gallery - Image Zoom
    **********************************/
    $('.zoom-image-hover').zoom();

    /***********************************
    * Gallery - Single Slider
    ************************************/
    $('.product-large-image-single-slider').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        focusOnSelect: true,
        arrows: true,
        prevArrow: '<button type="button" class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-left prevArrow"><i class="fa fa-angle-left"></i></button>',
        nextArrow: '<button type="button"  class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-right nextArrow"><i class="fa fa-angle-right"></i></button>',
        responsive: [

            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2,
                    arrows: false,
                    autoplay: true,
                    infinite: true,
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    arrows: false,
                    autoplay: true,
                    infinite: true,
                }
            }
        ]
    });

    /***********************************
    * Modal  Quick View Image
    ************************************/
   $('.modal-product-image-large').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.modal-product-image-thumb'
    });
    $('.modal-product-image-thumb').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        asNavFor: '.modal-product-image-large',
        focusOnSelect: true,
        prevArrow: '<button type="button" class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-left prevArrow"><i class="fa fa-angle-left"></i></button>',
        nextArrow: '<button type="button"  class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-right nextArrow"><i class="fa fa-angle-right"></i></button>',
    });
    $('.modal').on('shown.bs.modal', function (e) {
        $('.modal-product-image-large, .modal-product-image-thumb').slick('setPosition');
        $('.product-details-gallery-area').addClass('open');
    });

    /***********************************
    * Blog - Slider
    ************************************/
   $('.blog-image-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        focusOnSelect: true,
        arrows: true,
        prevArrow: '<button type="button" class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-left prevArrow"><i class="fa fa-angle-left"></i></button>',
        nextArrow: '<button type="button"  class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-right nextArrow"><i class="fa fa-angle-right"></i></button>',
    });

    /***********************************
    * Testimonial - Slider
    ************************************/
   $('.testimonial-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        focusOnSelect: true,
        dots: true,
        arrows: false,
    });

    /************************************************
     * Nice Select
     ***********************************************/
    $('select').niceSelect();

    /************************************************
     * Price Slider
     ***********************************************/
    $( "#slider-range" ).slider({
        range: true,
        min: 0,
        max: 500,
        values: [ 75, 300 ],
        slide: function( event, ui ) {
          $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
        }
      });
      $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
        " - $" + $( "#slider-range" ).slider( "values", 1 ) );


    /************************************************
     * Video  Popup
     ***********************************************/
    $('.video-play-btn').venobox(); 

    /************************************************
    * Animate on Scroll
    ***********************************************/
    AOS.init({
        // Settings that can be overridden on per-element basis, by `data-aos-*` attributes:
        duration: 1000, // values from 0 to 3000, with step 50ms
        once: true, // whether animation should happen only once - while scrolling down
        easing: 'ease',
    });
    window.addEventListener('load', AOS.refresh);
    /************************************************
     * Scroll Top
     ***********************************************/
    $('body').materialScrollTop();

 
})(jQuery);

