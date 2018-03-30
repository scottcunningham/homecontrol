import React, { Component } from 'react';
import './App.css';
import { BrowserRouter, Route, Link } from 'react-router-dom';
import {
  PlugPanel,
  MediaControlPanel,
  TrackPanel,
  HoldingPage,
} from './HomeControlComponents';

class MainApp extends Component {
  render() {
    return (
      <BrowserRouter>
        <div>
          <div id="header" class="container">
            <div class='col two'>
              <Link className="btn btn-rouge" to="/">::</Link>
            </div>
            <div class='col two'>
              <Link className="btn btn-rouge" to="/plugs">plugs</Link>
            </div>
            <div class='col two'>
              <Link className="btn btn-rouge" to='/media'>media</Link>
            </div>
            <div class='col two'>
              <Link className="btn btn-rouge" to='/tracks'>tracks</Link>
            </div>
          </div>

          <div class="container">
            <Route exact path="/" component={HoldingPage} />
            <Route path="/plugs" component={PlugPanel} />
            <Route path="/media" component={MediaControlPanel} />
            <Route path="/tracks" component={TrackPanel} />
          </div>
        </div>
      </BrowserRouter>
    );
  }
}

export default MainApp;
