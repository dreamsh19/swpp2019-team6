import React from 'react';
import { Provider } from 'react-redux';
import { mount } from 'enzyme';

import App from './App';
import { getMockStore } from './test-utils/mocks';
import { history } from './store/store';


const mockStore = getMockStore({}, {}, {});

jest.mock('./pages/LoginPage', () => {
  return jest.fn((props) => {
    return (<div className="loginPage" />);
  });
});
jest.mock('./pages/MainPage', () => {
  return jest.fn((props) => {
    return (<div className="mainPage" />);
  });
});
jest.mock('./pages/SignupPage', () => {
  return jest.fn((props) => {
    return (<div className="signupPage" />);
  });
});
jest.mock('./pages/CreateTravel', () => {
  return jest.fn((props) => {
    return (<div className="createTravel" />);
  });
});
jest.mock('./pages/EditTravel', () => {
  return jest.fn((props) => {
    return (<div className="editTravel" />);
  });
});
jest.mock('./pages/TravelDetail', () => {
  return jest.fn((props) => {
    return (<div className="travelDetail" />);
  });
});
jest.mock('./pages/SearchPage', () => {
  return jest.fn((props) => {
    return (<div className="searchPage" />);
  });
});
jest.mock('./pages/UserInfoPage', () => {
  return jest.fn((props) => {
    return (<div className="UserInfoPage" />);
  });
});

describe('App', () => {
  let app;

  beforeEach(() => {
    app = (
      <Provider store={mockStore}>
        <App history={history} store={mockStore} />
      </Provider>
    );
  });

  it('should render App.js', () => {
    const component = mount(app);
    expect(component.find('.App').length).toBe(1);
  });

  it('should render login', () => {
    history.push('/login');
    const component = mount(app);
    expect(component.find('.loginPage').length).toBe(1);
  });

  it('should render default', () => {
    history.push('/');
    const component = mount(app);
    expect(component.find('.loginPage').length).toBe(1);
  });

  it('should render signup', () => {
    history.push('/sign_up');
    const component = mount(app);
    expect(component.find('.signupPage').length).toBe(1);
  });

  it('should render signup', () => {
    history.push('/main');
    const component = mount(app);
    expect(component.find('.mainPage').length).toBe(1);
  });

  it('should render create travel', () => {
    history.push('/travel/create');
    const component = mount(app);
    expect(component.find('.createTravel').length).toBe(1);
  });

  it('should render edit travel', () => {
    history.push('/travel/0/edit');
    const component = mount(app);
    expect(component.find('.editTravel').length).toBe(1);
  });

  it('should render travel detail', () => {
    history.push('/travel/0/');
    const component = mount(app);
    expect(component.find('.travelDetail').length).toBe(1);
  });

  it('should render search', () => {
    history.push('/search/TEST/');
    const component = mount(app);
    expect(component.find('.searchPage').length).toBe(1);
  });

  it('should render user info', () => {
    history.push('/user/id');
    const component = mount(app);
    expect(component.find('.UserInfoPage').length).toBe(1);
  });

  it('should render error', () => {
    history.push('/error');
    const component = mount(app);
    expect(component.find('#error').length).toBe(1);
  });
});
