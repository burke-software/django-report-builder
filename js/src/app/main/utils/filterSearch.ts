import { IReport } from '../api.interfaces';

 export const filterSearch = (reports: IReport[], searchTerm: string) => {
    if (!searchTerm) {
      return reports;
    }
    const term = searchTerm.toLowerCase();
    return reports.filter((report) => {
      let name = report.name;
      if (name) {
        name = name.toLowerCase();
      }
      return name.indexOf(term) >= 0;
    });
};
