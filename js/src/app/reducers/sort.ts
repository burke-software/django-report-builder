import { IReport } from '../api.interfaces';

export const sortReports = (sortBy: string, reports: IReport[], ascending: boolean) => {
    console.log(sortBy);
    console.log(ascending);
    if (sortBy === '') {
        return reports;
    }

    const sortArray = reports.slice(0);

    if (sortBy === 'name' && ascending) {
        console.log('asc');
        return sortArray.sort((a, b) => {
            const x = a.name.toLowerCase();
            const y = b.name.toLowerCase();
            // if (ascending) {
                if (x < y) { return -1; }
                if (x > y) { return 1; }
            // }
            // else {
            //     if (x < y) { return 1; }
            //     if (x > y) { return -1; }
            // }
            return 0;
        });
    }
    if (sortBy === 'name' && !ascending) {
        console.log('desc');
        return sortArray.sort((a, b) => {
            const x = a.name.toLowerCase();
            const y = b.name.toLowerCase();
            // if (ascending) {
                if (x < y) { return 1; }
                if (x > y) { return -1; }
            // }
            // else {
            //     if (x < y) { return 1; }
            //     if (x > y) { return -1; }
            // }
            return 0;
        });
    }
    // else if (sortBy === 'date') {
    //     return sortArray.sort((a, b) => {
    //         const x = a.modified.toLowerCase();
    //         const y = b.modified.toLowerCase();
    //         if (ascending) {
    //             if (x < y) { return -1; }
    //             if (x > y) { return 1; }
    //         } else {
    //             if (x < y) { return 1; }
    //             if (x > y) { return -1; }
    //         }
    //         return 0;
    //     });
    // } else if (sortBy === 'user') {
    //     return sortArray.sort((a, b) => {
    //         const x = a.user_created.first_name.toLowerCase();
    //         const y = b.user_created.first_name.toLowerCase();
    //         if (ascending) {
    //             if (x < y) { return -1; }
    //             if (x > y) { return 1; }
    //         } else {
    //             if (x < y) { return 1; }
    //             if (x > y) { return -1; }
    //         }
    //         return 0;
    //     });
    // }
};
