let temporarySnotify: any = null;
const notify = (
  snotifyInstance: any,
  type: NotificationType,
  message: string
) => {
  switch (type) {
    case NotificationType.OK:
      {
        if (temporarySnotify) {
          snotifyInstance.remove(temporarySnotify.id);
        }
        snotifyInstance.success(message, {
          showProgressBar: false
        });
      }
      break;
    case NotificationType.ERROR:
      {
        if (temporarySnotify) {
          snotifyInstance.remove(temporarySnotify.id);
        }
        snotifyInstance.error(message, {
          timeout: 0,
          showProgressBar: false,
          closeOnClick: true
        });
      }
      break;
    case NotificationType.INFO:
      {
        temporarySnotify = snotifyInstance.info(message, {
          timeout: 1000,
          showProgressBar: true,
          closeOnClick: true,
          pauseOnHover: true
        });
      }
      break;
  }
};

export enum NotificationType {
  OK = 0,
  ERROR = 1,
  INFO = 2
}

export { notify };
