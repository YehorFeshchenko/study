import { BaseEntity } from 'typeorm';
export default class Contact extends BaseEntity {
    id: number;
    firstName: string;
    lastName: string;
    phoneNumber: number;
    isActive: boolean;
}
