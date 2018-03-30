import React, { Component } from 'react';
import FontAwesome from 'react-fontawesome';

class HomeControlButton extends Component {
  constructor(props) {
    super(props);
    this.state = {
      currentState: "dummy initial value"
    };
    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    e.preventDefault();
  }

  renderInner() {
    return (
      <a>
        <FontAwesome name={this.props.faClass}/>
        {this.props.name}
      </a>
    )
  }

  render() {
    return (
      <div className={`col ${this.props.size || 'three'}`}>
        <div className="btn btn-sea" onClick={this.handleClick}>
          {this.renderInner()}
        </div>
      </div>
    );
  }
}

class PlugButton extends HomeControlButton {
  buttonType() {
    return "plug";
  }

  constructor(props) {
    super(props);
    this.state = {
      status: false,
    };
  }

  componentDidMount() {
    fetch(`http://192.168.0.15/plugs/status/${this.props.plugName}`)
      .then((resp) => resp.json())
      .then(data => {
        this.setState({
          status: data.status
        })
      });
  }

  handleClick(e) {
    super.handleClick(e);
    fetch(`http://192.168.0.15/plugs/toggle/${this.props.plugName}`)
      .then((resp) => resp.json())
      .then(data => {
        this.setState({
          status: data.status
        })
      });
  }
}

class MediaButton extends HomeControlButton {
  buttonType() {
    return "media";
  }

  renderInner() {
    return (
      <a>
        <FontAwesome name={this.props.faClass}/>
      </a>
    )
  }

  handleClick() {
    fetch(this.url())
        .then((resp) => resp.json())
        .then(data => {
          if (this.props.callbackFromParent) {
            this.props.callbackFromParent(data);
          }
        });
  }

  url() {
    return `http://192.168.0.15/vol/${this.props.name}`
  }
}

class LinkButton extends HomeControlButton {
  buttonType() {
    return "link";
  }

  constructor(props) {
    super(props);
    this.state = {
      currentState: "dummy initial value"
    };
    this.link = props.link;
  }
}

class TvAppButton extends HomeControlButton {
  buttonType() {
    return "tv";
  }

  handleClick() {
    fetch(this.url())
        .then((resp) => resp.json())
        .then(data => {
          console.log(data);
        });
  }

  url() {
    return `/tv/open/${this.props.app}`
  }

}

export { MediaButton, PlugButton, LinkButton, TvAppButton };
