import { IField, IReport, IRelatedField } from '../../models/api';

export const setSearch = (
  searchArray: (IField | IReport | IRelatedField)[],
  searchTerm: string
) => {
  if (!searchTerm) {
    return searchArray;
  }

  const isIRelatedField = (
    object: IField | IReport | IRelatedField
  ): object is IRelatedField => {
    return 'verbose_name' in object;
  };

  const term = searchTerm.toLowerCase();
  return searchArray.filter(report => {
    let name;
    if (isIRelatedField(report)) {
      name = report.verbose_name;
    } else {
      name = report.name;
    }

    if (name) {
      name = name.toLowerCase();
    }
    return name.indexOf(term) >= 0;
  });
};
