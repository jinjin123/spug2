/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { makeRoute } from "../../libs/router";
import Template from './template';
import Task from './task';


export default [
  makeRoute('/template', Template),
  makeRoute('/task', Task),
]
