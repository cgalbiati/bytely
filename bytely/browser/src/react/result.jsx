'use strict';

import React from 'react';
import Loader from './load.jsx';

const BASE_URL = (process.env.BASE_URL || 'http://localhost:') + (process.env.port || '8000') + '/';


function Result(props){
  console.log('lala', props, props.err)

  //show loader while request is being processed
  if (props.loading === true){
    return (
      <div>
        <p> Making short url... please enjoy this cat while you wait.</p>
        <Loader/>
      </div>
    )
  }

  //show link if link has been returned
  else if (props.hash) {
    let shortLink = BASE_URL + props.hash;
    return (
      <div>
        <p> Here is your short url: 
          <a href={shortLink}>
            {shortLink}
          </a>
        </p>
      </div>
      )
  }

  //show error message if ajax returns with error
  else if (props.err) {
    return (
      <div>
        <p> Opps, something went wrong.  Please try again. </p>
      </div>
      )
  }

  // default: show instructions
  else {
    return (
      <div >
        <p> Enter a URL to shorten</p>
      </div>
    )
  }
  
};

export default Result;