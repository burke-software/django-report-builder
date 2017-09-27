interface IContentType {
  'pk': number;
  'name': string;
}

export type ContentTypeResponse = IContentType[];

export interface IReportDetailed {
    'id': number;
    'name': string;
    'description': string;
    'modified': string;
    'root_model': number;
    'root_model_name': string;
    'displayfield_set': any[];
    'distinct': boolean;
    'user_created': number;
    'user_modified': any;
    'filterfield_set': any[];
    'report_file': any;
    'report_file_creation': any;
}

interface IUser {
    'first_name': string;
    'last_name': string;
    'id': number;
}

export interface IReport {
    'id': number;
    'name': string;
    'modified': string;
    'root_model': number;
    'root_model_name': string;
    'user_created': IUser;
}

export type ReportsResponse = IReport[];
