/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { makeRoute } from 'libs/router';
import Environment from './environment';
import Service from './service';
import RancherConf from './rancherconfmap';
import App from './app';
import Setting from './setting';


export default [
  makeRoute('/environment', Environment),
  makeRoute('/service', Service),
  makeRoute('/app', App),
  makeRoute('/rancherconf', RancherConf),
  makeRoute('/setting/:type/:id', Setting),
]
