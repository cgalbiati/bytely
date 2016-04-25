'use strict';
import React from 'react';

// shows a loading image while waiting on requests
// I made this its own component because it seemed like the kind of thing that would be re-used, 
//even though I probably won't reuse it in this small app
function Loader (props){
  return (
    <div >
      <img className='loader-img' src="http://i.imgur.com/ssjmxXz.gif"/>

      
    </div>
  )
};

export default Loader;



// <img className='loader-img' style="-webkit-user-select: none" src="http://cdn.themetapicture.com/pic/images/2014/08/25/funny-gif-cat-washing-machine.gif">

//      <img className='loader-img' src="http://www.smopic.com/wp-content/uploads/2012/09/Small-kitten-chasing-its-tail-do-not-know-the-cat-will-dizziness-it.gif"/>
