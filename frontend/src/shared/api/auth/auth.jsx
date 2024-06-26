import { axiosClient } from "@shared/api/axiosClient";

export async function authLogin(params) {
  try {
    const { username, password } = params;
    const response = await axiosClient
      .post("/auth/login/", {
        username: username,
        password: password,
      })
      .then((response) => response.data);
    return response;
  } catch (error) {
    console.error(error);
  }
}

export async function authRegister(params) {
  try {
    const { username, password } = params;
    const response = await axiosClient
      .post("/auth/register/", {
        username: username,
        password: password,
      })
      .then((response) => response.data);
    return response;
  } catch (error) {
    console.error(error);
  }
}
