import axios, { AxiosRequestConfig } from 'axios';
import { buildPatchModifierPayload } from './patchHelper';
import { GemSearchApiModel } from '@/objects/apiModels/GemSearchApiModel';
import { Gem } from '@/objects/Gem';
import { GemSaveApiModel } from '@/objects/apiModels/GemSaveApiModel';
import { Tag } from '@/objects/Tag';
import { LoginApiModel } from '@/objects/apiModels/LoginApiModel';
import { LoginResult } from '@/objects/LoginResult';

export default class AppService {
  private serviceRootUrl: string;
  constructor() {
    axios.defaults.baseURL = '/';
    axios.interceptors.request.use(this.axiosInterceptor);
    this.serviceRootUrl = process.env.VUE_APP_APIURL;
  }
  public axiosInterceptor = (config: AxiosRequestConfig) => {
    if (typeof window === 'undefined') {
      return config;
    }
    const token = window.localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  };

  public getGems(gemSearchQuery: GemSearchApiModel): Promise<Gem[]> {
    return new Promise((resolve, reject) => {
      axios
        .post(`${this.serviceRootUrl}/gems/search`, gemSearchQuery)
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }

  public createGem(gemCreationApiModel: GemSaveApiModel) {
    return new Promise((resolve, reject) => {
      axios
        .post(`${this.serviceRootUrl}/gems`, gemCreationApiModel)
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }

  public updateGem(gemSaveApiModel: GemSaveApiModel) {
    return new Promise<Gem>((resolve, reject) => {
      const patchModel = gemSaveApiModel.buildPatchModel();
      axios
        .patch(`${this.serviceRootUrl}/gems/${gemSaveApiModel.id}`, patchModel)
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }
  public getGemById(gemId: number): Promise<Gem> {
    return new Promise((resolve, reject) => {
      axios
        .get(`${this.serviceRootUrl}/gems/${gemId}`)
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }
  public deleteGem(gemId: number) {
    return new Promise((resolve, reject) => {
      axios
        .delete(`${this.serviceRootUrl}/gems/${gemId}`)
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }
  public login(credentials: LoginApiModel): Promise<LoginResult> {
    return new Promise((resolve, reject) => {
      axios
        .post(`${this.serviceRootUrl}/auth/login`, credentials)
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }
  public getTags(text: string): Promise<Tag[]> {
    return new Promise((resolve, reject) => {
      axios
        .post(`${this.serviceRootUrl}/tags/search`, {
          text,
          limit: text ? 10 : 10000
        })
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }

  public deleteTag(tagId: number) {
    return new Promise((resolve, reject) => {
      axios
        .delete(`${this.serviceRootUrl}/tags/${tagId}`)
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }
  public replaceTagLabel(tagId: number, newLabel: string) {
    return new Promise((resolve, reject) => {
      axios
        .post(`${this.serviceRootUrl}/tags`, {
          tagId,
          newLabel
        })
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }
}
