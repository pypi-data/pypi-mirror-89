import React, { lazy, Suspense } from 'react';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { Provider } from 'react-redux';
import { HelmetProvider } from 'react-helmet-async';
import store from 'store';
import routes from 'routes';
import theme from 'theme/theme';
import GlobalStyle from 'theme/GlobalStyle';
import MainTemplate from 'templates/MainTemplate';
import CveSearch from 'views/CveSearch/CveSearch';
import RegistryScan from 'views/RegistryScan/RegistryScan';
import Loading from 'components/atoms/LoadingAnimation/LoadingAnimation';
import HomeView from './HomeView/HomeView';

const RemoteHostInfoSearch = lazy(
  () => import('views/RemoteHostInfo/RemoteHostInfoSearch'),
);
const RemoteHostInfoResult = lazy(
  () => import('views/RemoteHostInfo/RemoteHostInfoResult'),
);
const CveSearchResult = lazy(() => import('views/CveSearch/CveSearchResult'));
const RegistryScanResult = lazy(
  () => import('views/RegistryScan/RegistryScanResults'),
);
const ExploitsSearchView = lazy(
  () => import('views/ExploitSearch/ExploitSearchView'),
);
const ExploitsResultView = lazy(
  () => import('views/ExploitSearch/ExploitResultView'),
);
const SettingsView = lazy(() => import('views/Settings/SettingsView'));
const DocsView = lazy(() => import('views/DocsView/DocsView'));
const HardwareInfoScan = lazy(
  () => import('views/HardwareInfo/HardwareInfoScan'),
);
const HardwareInfoResult = lazy(
  () => import('views/HardwareInfo/HardwareInfoResult'),
);

const helmetContext = {};

function Root() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <ThemeProvider theme={theme}>
          <HelmetProvider context={helmetContext}>
            <GlobalStyle />
            <MainTemplate>
              <HomeView />
              <Suspense fallback={<Loading bigView />}>
                <Switch>
                  <Redirect exact from={routes.home} to={routes.homeRedirect} />
                  <Route
                    exact
                    path={routes.remoteHostInfo}
                    component={RemoteHostInfoSearch}
                  />
                  <Route
                    exact
                    path={routes.remoteHostInfoResult}
                    component={RemoteHostInfoResult}
                  />
                  <Route exact path={routes.cveSearch} component={CveSearch} />
                  <Route
                    exact
                    path={routes.cveSearchResults}
                    component={CveSearchResult}
                  />
                  <Route
                    exact
                    path={routes.registry}
                    component={RegistryScan}
                  />
                  <Route
                    exact
                    path={routes.registryResults}
                    component={RegistryScanResult}
                  />
                  <Route
                    exact
                    path={routes.exploits}
                    component={ExploitsSearchView}
                  />
                  <Route
                    exact
                    path={routes.exploitResults}
                    component={ExploitsResultView}
                  />
                  <Route
                    exact
                    path={routes.hardwareInfo}
                    component={HardwareInfoScan}
                  />
                  <Route
                    exact
                    path={routes.hardwareInfoResults}
                    component={HardwareInfoResult}
                  />
                  <Route
                    exact
                    path={routes.documentation}
                    component={DocsView}
                  />
                  <Route
                    exact
                    path={routes.settings}
                    component={SettingsView}
                  />
                </Switch>
              </Suspense>
            </MainTemplate>
          </HelmetProvider>
        </ThemeProvider>
      </BrowserRouter>
    </Provider>
  );
}

export default Root;
