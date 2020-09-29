import CreateContactDto from "../../dto/create-contact.dto";
import Contact from './contact.entity';
import { ContactsService } from './contacts.service';
export declare class ContactsController {
    private readonly contactsService;
    constructor(contactsService: ContactsService);
    findAll(): Promise<{
        contactsList: Contact[];
    }>;
    create(createContactDto: CreateContactDto): Promise<Contact>;
    find_by_id(id: string): Promise<{
        hasContact: boolean;
        firstName?: undefined;
        lastName?: undefined;
        phoneNumber?: undefined;
        address?: undefined;
        username?: undefined;
        email?: undefined;
    } | {
        firstName: any;
        lastName: any;
        phoneNumber: any;
        address: any;
        username: any;
        email: any;
        hasContact: boolean;
    }>;
    creating(): void;
    remove(id: string): Promise<{
        hasContact: boolean;
        firstName?: undefined;
        lastName?: undefined;
        phoneNumber?: undefined;
        address?: undefined;
        username?: undefined;
        email?: undefined;
    } | {
        firstName: any;
        lastName: any;
        phoneNumber: any;
        address: any;
        username: any;
        email: any;
        hasContact: boolean;
    }>;
}
