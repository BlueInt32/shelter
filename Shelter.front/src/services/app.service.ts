import axios, { AxiosRequestConfig } from 'axios';
import { buildPatchModifierPayload } from './patchHelper';
import { SearchForElementsApiModel } from '@/objects/apiModels/SearchForElementsApiModel';
import { Element } from '@/objects/Element';
import {
  SaveElementBaseApiModel,
  SaveElementWithFileApiModel,
  SaveElementWithLinkApiModel
} from '@/objects/apiModels/SaveElementApiModel';
import { Tag } from '@/objects/Tag';
import { LoginApiModel } from '@/objects/apiModels/LoginApiModel';
import { LoginResult } from '@/objects/LoginResult';
import { SearchForTagsApiModel } from '@/objects/apiModels/SearchForTagsApiModel';
import { ElementType } from '@/objects/apiModels/ElementType';

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

  public searchForElements(
    searchForElementsApiModel: SearchForElementsApiModel
  ): Promise<Element[]> {
    return new Promise((resolve, reject) => {
      axios
        .get(`${this.serviceRootUrl}/elements`)
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }

  public createElementWithLink(
    data: SaveElementWithLinkApiModel
  ): Promise<Element> {
    return new Promise((resolve, reject) => {
      const creationApiType = this.resolveCreationApiSegmentFromElementType(
        data.type
      );
      axios
        .post(`${this.serviceRootUrl}/${creationApiType}`, data)
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }

  public createElementWithFile(
    data: SaveElementWithFileApiModel
  ): Promise<Element> {
    return new Promise((resolve, reject) => {
      let payloadWithoutFile = Object.assign({}, data);
      delete payloadWithoutFile.file;
      delete payloadWithoutFile.type;

      const json = JSON.stringify(payloadWithoutFile);
      const blob = new Blob([json], {
        type: 'application/json'
      });
      var formData = new FormData();
      formData.append('payload', blob);
      if (data.file) {
        formData.append('file', data.file);
      }
      const creationApiType = this.resolveCreationApiSegmentFromElementType(
        data.type
      );
      axios
        .post(`${this.serviceRootUrl}/${creationApiType}`, formData)
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }

  private resolveCreationApiSegmentFromElementType(elementType: ElementType) {
    switch (elementType) {
      case ElementType.ImageLink:
        return 'image-links';
      case ElementType.ImageFile:
        return 'image-files';
      case ElementType.VideoLink:
        return 'video-links';
      case ElementType.VideoFile:
        return 'video-files';
      case ElementType.WebLink:
        return 'web-links';
    }
    return 'elements';
  }

  public updateElementWithFile(data: SaveElementWithFileApiModel) {
    return new Promise<Element>((resolve, reject) => {
      let payloadWithoutFile = Object.assign({}, data);
      delete payloadWithoutFile.file;
      delete payloadWithoutFile.type;

      const json = JSON.stringify(payloadWithoutFile);
      const blob = new Blob([json], {
        type: 'application/json'
      });
      var formData = new FormData();
      formData.append('payload', blob);
      if (data.file) {
        formData.append('file', data.file);
      }
      const creationApiType = this.resolveCreationApiSegmentFromElementType(
        data.type
      );
      axios
        .put(`${this.serviceRootUrl}/${creationApiType}/${data.id}`, formData)
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }
  public updateElementWithLink(data: SaveElementBaseApiModel) {
    const creationApiType = this.resolveCreationApiSegmentFromElementType(
      data.type
    );
    return new Promise<Element>((resolve, reject) => {
      axios
        .put(`${this.serviceRootUrl}/${creationApiType}/${data.id}`, data)
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }
  public getElementById(elementId: number): Promise<Element> {
    return new Promise((resolve, reject) => {
      axios
        .get(`${this.serviceRootUrl}/elements/${elementId}`)
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.response.data.message);
        });
    });
  }
  public getElementFileUrlById(elementId: number): string {
    return `${this.serviceRootUrl}/elements/file/${elementId}`;
  }
  public getElementThumbnailFileUrlById(elementId: number): string {
    return `${this.serviceRootUrl}/elements/thumbnail/${elementId}`;
  }
  public deleteElement(elementId: number) {
    return new Promise((resolve, reject) => {
      axios
        .delete(`${this.serviceRootUrl}/elements/${elementId}`)
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
  public searchForTags(model: SearchForTagsApiModel): Promise<Tag[]> {
    return new Promise((resolve, reject) => {
      axios
        .get(`${this.serviceRootUrl}/tags/search/${model.labelSearchText}`)
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
