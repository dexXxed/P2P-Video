/*
Theme Name: CETUS – Creative Portfolio HTML5 Template
Theme URI: http://live.envalab.com/html/cetus
Author: ENVALAB
Author URI: https://themeforest.net/user/envalab/portfolio
Description: CETUS is minimal multi-purpose portfolio template suitable any agencies, portfolios, creative group, freelancers, artists, professionals and much more.
Version: 1.0
*/

(function($) {
    "use strict";
	
	/*----------------------------
    START - Main menu responsive
    ------------------------------ */
	$('.responsive-menu-show').on('click', function(){
		$(this).hide();
		$('.responsive-menu-hidden').show();
		$('.menubar-ul').show();
	});
	$('.responsive-menu-hidden').on('click', function(){
		$(this).hide();
		$('.responsive-menu-show').show();
		$('.menubar-ul').hide();
        $('.menubar-ul li.menuclick-dropdown-li a').parent().removeClass('has-active-dropdown');
		$('.menubar-ul li.menuclick-lii a.menuclick-lii-a').parent().removeClass('has-active');
	});
	$('.menubar-ul li.menuclick-lii a').addClass('menuclick-lii-a');
	$('.menubar-ul li.menuclick-dropdown-li a').removeClass('menuclick-lii-a');
	$('.menubar-ul li.menuclick-lii a.menuclick-lii-a').on('click', function () {
		$(this).parent().toggleClass('has-active');
        $(this).closest('li').siblings('.menuclick-lii').removeClass('has-active');
        $(this).closest('li').siblings('.menuclick-lii').toggleClass('has-inactive');
		$(this).parent().removeClass('has-inactive');
        $('.menubar-ul li.menuclick-dropdown-li a').parent().removeClass('has-active-dropdown');
    });
	$('.menubar-ul li.menuclick-dropdown-li a').on('click', function () {
		$(this).parent().toggleClass('has-active-dropdown');
		$(this).parent().removeClass('has-active');
        $(this).closest('li').siblings('.menuclick-dropdown-li').removeClass('has-active-dropdown');
        $(this).closest('li').siblings('.menuclick-dropdown-li').toggleClass('has-inactive-dropdown');
		$(this).parent().removeClass('has-inactive-dropdown');
    });
	
	/*----------------------------
    START - Slider
    ------------------------------ */
	var portfolioSlider = $('.portfolio-item');
	portfolioSlider.owlCarousel({
		loop:true,
		dots:true,
		autoplay: false,
		autoplayTimeout:4000,
		nav: true,
		navText: ["<i class='fa fa-long-arrow-left'></i>", "<i class='fa fa-long-arrow-right'></i>"],
		items: 1,
	});
	portfolioSlider.on('changed.owl.carousel', function(property) {
		var current = property.item.index;
		var prevThumb = $(property.target).find(".owl-item").eq(current).prev().find("img").attr('src');
		var nextThumb = $(property.target).find(".owl-item").eq(current).next().find("img").attr('src');
		$('.thumb-prev').find('img').attr('src', prevThumb);
		$('.thumb-next').find('img').attr('src', nextThumb);
	});
	$('.thumb-next img').on('click', function() {
		portfolioSlider.trigger('next.owl.carousel', [300]);
		return false;
	});
	$('.thumb-prev img').on('click', function() {
		portfolioSlider.trigger('prev.owl.carousel', [300]);
		return false;
	});
	$(".style-slide").owlCarousel({
		items: 1,
		dots: true,
		loop: true,
		autoplay: true,
		nav: true,
		navText: ["<i class='fa fa-long-arrow-left'></i>", "<i class='fa fa-long-arrow-right'></i>"],
	});
	
	/*----------------------------
    START - Preloader
    ------------------------------ */
	jQuery(window).on('load', function(){
		jQuery("#preloader").fadeOut(2000);
	});
	
	/*----------------------------
    START - Scroll to Top
    ------------------------------ */
	$(window).on('scroll', function() {
		if ($(this).scrollTop() > 500) {
			$('.scrollToTop').show();
		} else {
			$('.scrollToTop').hide();
		}
	});
	$('.scrollToTop').on('click', function () {
		$('html, body').animate({scrollTop : 0},2000);
		return false;
	});
	
	/*----------------------------
    START - WOW JS animation
    ------------------------------ */
	new WOW().init();

})(jQuery);