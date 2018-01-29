// import { IField, IReport, IRelatedField } from '../../api.interfaces';

 export const setSearch = (searchArray: any[], searchTerm: string) => {

    if (!searchTerm) {
      return searchArray;
    }

    const term = searchTerm.toLowerCase();
    return (searchArray.filter((report) => {

      let name;
      Object.keys(searchArray[0]).includes('verbose_name') ? 
      name = report.verbose_name : name = report.name;

      if (name) {
        name = name.toLowerCase();
      }
      return name.indexOf(term) >= 0;
    }));
};
