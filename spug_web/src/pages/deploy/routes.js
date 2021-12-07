/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { makeRoute } from "../../libs/router";
import app from './app';
import request from './request';
import rancherioc from './rancherioc';
import rancherfangyi from './rancherfangyi';

import notice from './notice';
import doExt1Index from './do/Ext1Index';
import doExt2Index from './do/Ext2Index';
import doExt2Rancher from './do/Ext2Rancher';


export default [
  makeRoute('/app', app),
  makeRoute('/request', request),
  makeRoute('/rancherioc', rancherioc),
  makeRoute('/rancherfangyi', rancherfangyi),

  makeRoute('/rancher/notice', notice),
  makeRoute('/do/ext1/:id', doExt1Index),
  makeRoute('/do/ext2/:id', doExt2Index),
  makeRoute('/do/ext1/:id/:log', doExt1Index),
  makeRoute('/do/ext2/:id/:log', doExt2Index),
  makeRoute('/do/rancher/:id/:log', doExt2Rancher),

]
