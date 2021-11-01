/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { makeRoute } from 'libs/router';
import Environment from './environment';
import Project from './project';
import Cluster from './cluster';
import Portlist from './portlist';
import ServiceBag from './servicebag';
import Workzone from './workzone';
import Cuser from './cuser';
import Domain from './domainlist';

import Resource from './resourcet';

import Zone from './zone';
import Device from './devicepostion';
import Service from './service';
import RancherConf from './rancherconfmap';
import App from './app';
import Backup from './backup';
import Setting from './setting';


export default [
  makeRoute('/environment', Environment),
  makeRoute('/cuser', Cuser),
  makeRoute('/resouret', Resource),
  makeRoute('/domain', Domain),

  makeRoute('/project', Project),
  makeRoute('/cluster', Cluster),
  makeRoute('/portlist', Portlist),
  makeRoute('/servicebag', ServiceBag),
  makeRoute('/workzone', Workzone),
  makeRoute('/zone',Zone ),
  makeRoute('/device', Device),

  makeRoute('/service', Service),
  makeRoute('/backup', Backup),
  makeRoute('/app', App),
  makeRoute('/rancherconf', RancherConf),
  makeRoute('/setting/:type/:id', Setting),
]
