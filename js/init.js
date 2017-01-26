$(document).ready(function() {
	$('#fullpage').fullpage({
		slidesNavigation: true,
		keyboardScrolling: true,
		// fadingEffect: true,
		paddingBottom: '5vh',
		controlArrows: true,
		// scrollHorizontally: true,
		// dragAndMove: true,

		onSlideLeave: function(anchorLink, index, slideIndex, direction, nextSlideIndex){
			console.log( anchorLink, index, slideIndex, direction, nextSlideIndex );
		}

	});

});
