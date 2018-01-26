import { IReport } from '../api.interfaces';

export const sortReports = (sortBy: string, reports: IReport[]) => {
    if (sortBy === '') {
        return reports;
    }

    let nameCount = true;

    const sortArray = reports.slice(0);

    if (sortBy === 'name' && nameCount) {
        console.log('sort');
        nameCount = !nameCount;
        return sortArray.sort((a, b) => {
            const x = a.name.toLowerCase();
            const y = b.name.toLowerCase();
            if (x < y) { return -1; }
            if (x > y) { return 1; }
            return 0;
        });
    } else if (sortBy === 'name' && !nameCount) {
        nameCount = !nameCount;
        console.log('reverse');
        return sortArray.sort((a, b) => {
            const x = a.name.toLowerCase();
            const y = b.name.toLowerCase();
            if (x < y) { return 1; }
            if (x > y) { return -1; }
            return 0;
        });
    } else if (sortBy === 'date') {
        return sortArray.sort((a, b) => {
            const x = a.modified.toLowerCase();
            const y = b.modified.toLowerCase();
            if (x < y) { return 1; }
            if (x > y) { return -1; }
            return 0;
        });
    } else if (sortBy === 'user') {
        return sortArray.sort((a, b) => {
            const x = a.user_created.first_name.toLowerCase();
            const y = b.user_created.first_name.toLowerCase();
            if (x < y) { return -1; }
            if (x > y) { return 1; }
            return 0;
        });
    }
};
