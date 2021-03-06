import React, { Component } from 'react';
import HeaderContainer from '../containers/common/HeaderContainer';
import UserInfoSectionContainer from '../containers/user-info/UserInfoSectionContainer';
import UserTravelOverviewList from '../containers/travel-overview/UserTravelOverviewList';
import CollaboratorTravelOverviewList from '../containers/travel-overview/CollaboratorTravelOverviewList';

class UserInfoPage extends Component {
  state = {
    currentUser: JSON.parse(localStorage.getItem('user')),
    is_mypage: false,
  }

  componentDidMount() {
    this.setState((prevState) => (
      { is_mypage: (prevState.currentUser.id === parseInt(this.props.match.params.id, 10)) }
    ));
  }


  render() {
    return (
      <div className="userInfoPage">
        <HeaderContainer />
        <UserInfoSectionContainer
          id={this.props.match.params.id}
          is_mypage={this.state.is_mypage}
        />
        <div
          style={{
            marginLeft: 24,
            marginRight: 24,
          }}
        >
          <UserTravelOverviewList
            id={this.props.match.params.id}
            is_mypage={this.state.is_mypage}
          />
          {this.state.is_mypage ? (
            <CollaboratorTravelOverviewList
              id={this.props.match.params.id}
              is_mypage={this.state.is_mypage}
            />
          ) : (
            <span />
          )}
        </div>
      </div>
    );
  }
}

export default UserInfoPage;
