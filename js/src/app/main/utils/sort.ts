import { IReport } from '../../api.interfaces';

export const sortReports = (sortBy: string, reports: IReport[], ascending: boolean) => {

    if (sortBy === '') {
        return reports;
    }

    const sortArray = reports.slice(0);

            if (sortBy === 'user') {
                return sortArray.sort((a, b) => {
                    const x = a.user_created.first_name.toLowerCase();
                    const y = b.user_created.first_name.toLowerCase();
                    if (ascending) {
                        if (x < y) { return -1; }
                        if (x > y) { return 1; }
                    } else {
                        if (x < y) { return 1; }
                        if (x > y) { return -1; }
                    }
                    return 0;
                });
            }

            return sortArray.sort((a, b) => {
                const x = a[sortBy].toLowerCase();
                const y = b[sortBy].toLowerCase();
                if (ascending) {
                    if (x < y) { return -1; }
                    if (x > y) { return 1; }
                } else {
                    if (x < y) { return 1; }
                    if (x > y) { return -1; }
                }
                return 0;
            });
};
