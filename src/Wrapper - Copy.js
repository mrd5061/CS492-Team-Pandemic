import React, { Component } from 'react';
import App from './app';

import axios from 'axios'

export default class Wrapper extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isMobileView: false,
      selectedFile: null,
      uploaded: false,
      useDefault: false,
      clicked: false,
      flnm: ""
    }
  }

  componentDidMount() {
    if (document.documentElement.clientWidth <= 700 || document.documentElement.clientHeight <=500) {
      this.setState({ isMobileView: true })
    } else {
      this.setState({ isMobileView: false })
    }
    window.addEventListener('resize', this.handleResize);
  }

  handleResize = () => {
    if (document.documentElement.clientWidth <= 700 || document.documentElement.clientHeight <=500) {
      this.setState({ isMobileView: true })
    } else {
      this.setState({ isMobileView: false })
    }
  }

  handleChange = e => {
    this.setState({ selectedFile: e.target.files[0], flnm: e.target.files[0].name })
  }

  handleUseDefault = (e) => {
    this.setState({ useDefault: true });
  }

  
  render() {
    return (
      <>
        {
          this.state.isMobileView ? (
            <div className="upload-form-wrapper">
              <p>Please open it in bigger window.</p>
            </div>
          ) : (
              (this.state.uploaded || this.state.useDefault) ? (
                <App choice={this.state.uploaded ? 1 : 2} />
              ) : (
                  <div className="upload-form-wrapper">
                    <div className="heading">Example splash page. Click the button below for example data on coronavirus in the United States.</div>
                    <div className="upload-form">
                      <button style={{ backgroundColor: "#11BAEF" }} onClick={this.handleUseDefault} > Enter Site </button>
                    </div>
                  </div>
                )
            )
        }
      </>
    )
  }
}