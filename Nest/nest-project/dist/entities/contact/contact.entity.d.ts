import { BaseEntity } from 'typeorm';
export default class Contact extends BaseEntity {
    id: number;
    firstName: string;
    lastName: string;
    phoneNumber: number;
    email: string;
    address: string;
    username: string;
}
