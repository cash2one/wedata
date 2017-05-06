import axios from 'axios';

let base = "";

let baseURL = process.env.BASE_URL;

export const getOfficialAccountList = params => {
  return axios.get(`${baseURL}/accounts`, { params: params });
};
export const getArticleList = (name, params) => {
  return axios.get(`${baseURL}/account/` + name, { params: params });
}
