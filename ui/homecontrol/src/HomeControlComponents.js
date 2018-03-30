import React, { Component } from 'react';
import './App.css';
import { PlugButton, MediaButton, LinkButton } from './HomeControlButtons';
import logo from './logo.svg';

class PlugPanel extends Component {
  render() {
    return (
      <div className="container">
        <h1>plugs</h1>
        <div className="row">
          <PlugButton  name='Lamp'     faClass='eject' plugName='lamp'/>
          <PlugButton  name='Speakers' faClass='eject' plugName='speakers'/>
        </div>
      </div>
    )
  }
}

class LinkPanel extends Component {
  render() {
    return (
      <div className="container">
        <h1>links</h1>
        <div className="row">
          <LinkButton  name='Music' faClass='snowflake-o' link='/iris'/>
        </div>
      </div>
    )
  }
}

class AccountSelector extends Component {
  render() {
    return (
      <div>
        <select id="account-select" class="btn btn-sea col three">
            <option value="blurpl">scott</option>
            <option value="imorlowska">iza</option>
        </select>
      </div>
    )
  }
}

class VolumeDisplay extends Component {

  constructor(props) {
    super(props);
    this.state = {
      percent: 0,
      muted: false,
    }
    this.updateVolume();
  }

  updateVolume() {
    fetch("http://192.168.0.15/vol/get")
      .then((resp) => resp.json())
      .then(d => {
        this.setState({
          percent: d.percent,
          muted: d.muted,
        })
      });
  }

  render() {
      var mutedText = "";
      if (this.state.muted) {
        mutedText = "[muted]";
      }
      return (
        <p id="vol-current">
          {this.state.percent} {mutedText}
        </p>
      )
  }
}


class MediaControlPanel extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="all">
        <div className="container">
          <h1>media</h1>
          <div className="row">
            <MediaButton name='playpause'  size='two' faClass='play'/>
            <MediaButton name='track/prev' size='two' faClass='step-backward'/>
            <MediaButton name='track/next' size='two' faClass='step-forward'/>

            <MediaButton name='up'   size='two' callbackFromParent={(d) => this.updateVolumeDisplay(d)} faClass='volume-up'/>
            <MediaButton name='down' size='two' callbackFromParent={(d) => this.updateVolumeDisplay(d)} faClass='volume-down'/>
            <MediaButton name='mute' size='two' callbackFromParent={(d) => this.updateVolumeDisplay(d)} faClass='volume-off'/>
          </div>
          <VolumeDisplay ref="child"/>
      </div>
    </div>
    );
  }

  updateVolumeDisplay(d) {
    this.refs.child.setState({
      percent: d.percent,
      muted: d.muted,
    });
  }
}


class TrackPanel extends Component {
  render() {
    return (
      <div className="all">
          <div className="row">
            <AccountSelector />
            <MediaButton name='refresh' size='two' faClass='refresh'/>
          </div>
        <div id="scottframe">
          <iframe title="iris" src="http://192.168.0.15/iris"/>
        </div>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      </div>
    );
  }
}

class HoldingPage extends Component {
  render() {
    return (
      <div class="holdingPage">
      	<div class="container">
          <div class='row'>
            <div class='col twelve'>
              <h1>welcome to <a href="">orangepizero.local</a></h1>
            </div>
          </div>
        </div>

        <div class="container">
          <div class='row'>
            <div class='col twelve'>
              <img src={logo} className="logo" alt="logo" width="20%"/>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export { PlugPanel, LinkPanel, MediaControlPanel, HoldingPage, TrackPanel };
