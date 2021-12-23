/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { makeRoute } from "../../libs/router";
import NetTool from './index';


export default [
  makeRoute('/tool', NetTool),
]
