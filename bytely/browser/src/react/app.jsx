"use strict"
import React from 'react';
import UrlInput from './input.jsx';
import Result from './result.jsx';
import { ajax } from 'jquery';
import ReactDOM from 'react-dom';


/*
base structure for this.state
{
  loading: true/false
  url: str
  hash: str
  err: t/f
}

structure for app:
app
  input
  result (shows either short url, load or instructions)
    loader
    short link
    instructions
*/



const App = React.createClass({
  render: function () {
    return  (
      <div id='App'>
        <UrlInput 
          submitUrl={this.submitUrl}/>
        <Result 
          url={this.state.url} 
          hash={this.state.hash} 
          loading={this.state.loading} 
          err={this.state.err} />
      </div>
    )
  },

  getInitialState: function(){
    return {
      loading: false,
      hash: null,
      err: false
    };
  },

  submitUrl: function(url){
    console.log('submiting url', url)
    let self = this;
    //clear input, set loading
    this.setState({loading: true});
      ajax({
      url: 'shorten/',
      type: 'POST',
      data: url,
      success: function(data){
        self.setState({hash: data.short_url, loading: false});
        console.log('got data', data)
      },
      error: function(err){
        console.log('error shortening url', err);
        self.setState({err: true, loading: false});
      }
    });

  },











  // getEventsForTimeline: function(birthYear, endYear){
  //   var self = this;
  //   var url = "/api/range?min="+birthYear+"&max="+endYear+"&perYear=5";

  //   $.ajax({
  //     url: url,
  //     success: self.setEventsData,
  //     error: function(err){console.log(err)}
  //   });
  // },




  // setEventsData: function(data){
  //   var eventsList = {};
  //   data.forEach(function(event){
  //     if (eventsList[event.year]){
  //       eventsList[event.year].push(event);
  //     } else {
  //       eventsList[event.year] = [event];
  //     }
  //   });

  //   this.setState({events: eventsList});
  // },

  // getMoreEvents: function(year){
  //   var self = this;
  //   var url = "/api/year/" + year + '?limit=20';

  //   $.ajax({
  //     url: url,
  //     success: self.setAddlEvents,
  //     error: function(err){console.log(err);}
  //   });
  // },

  
});


export function renderApp(){
  //render react app
  ReactDOM.render(<App />, document.getElementById('react-app'));
}
